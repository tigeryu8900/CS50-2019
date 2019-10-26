import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required, lookup, usd
from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# Set locks to prevent race conditions
locks = {}

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    quote_cache = {}
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :id", id=session.get("user_id", ""))
    portfolio = []
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session.get("user_id", ""))[0]["cash"]
    total = cash
    for transaction in transactions:
        symbol = transaction.get("symbol", "N/A")
        shares = int(transaction.get("shares", "N/A"))
        if symbol == "_CASH_":
            continue
        quote = quote_cache.get(symbol, False)
        subtotal = None
        price = None
        if quote:
            price = quote.get("price_float", False)
            subtotal = price * shares
            i = 0
            while portfolio[i][0] != symbol:
                i += 1
            portfolio[i][2] += shares
            portfolio[i][4] += subtotal
        else:
            quote = lookup(symbol)
            quote_cache[symbol] = quote
            price = quote.get("price_float", False)
            subtotal = price * shares
            portfolio.append([symbol, quote.get("name"), shares, price, subtotal])
        total += subtotal
    for holdings in portfolio:
        holdings[3] = usd(holdings[3])
        holdings[4] = usd(holdings[4])
    return render_template("index.html", portfolio=portfolio, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET"])
@login_required
def get_buy():
    """Buy shares of stock"""
    return render_template("buy.html")


@app.route("/buy", methods=["POST"])
@login_required
def post_buy():
    """Buy shares of stock"""
    symbol = request.form.get("symbol", "")
    if not symbol:
        return apology("missing symbol")
    quote = lookup(symbol)
    if not isinstance(quote, dict):
        return apology("invalid symbol")

    sharesStr = request.form.get("shares", "")
    if not (sharesStr.isdigit() and int(sharesStr) > 0):
        return apology("shares must be a counting number")
    shares = int(sharesStr)

    while locks.get(session.get("user_id"), False):
        pass
    locks[session.get("user_id")] = True
    user = db.execute("SELECT * FROM users WHERE id = :id", id=session.get("user_id"))[0]
    price = quote.get("price_float")
    totalPrice = price * shares
    if user.get("cash") < totalPrice:
        locks.pop(session.get("user_id"), None)
        return apology("can't afford")
    db.execute("UPDATE users SET cash = cash - :totalPrice WHERE id = :id", totalPrice=totalPrice, id=session.get("user_id"))
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
               user_id=session.get("user_id"), symbol=quote.get("symbol"), shares=shares, price=price)
    locks.pop(session.get("user_id"), None)
    return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    data = username is not None and db.execute("SELECT id from users WHERE username = :username", username=username) == []
    return jsonify(data)
    #, (400, 200)[data]


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :id", id=session.get("user_id", ""))
    for t in transactions: t["price"] = usd(t["price"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/profile", methods=["GET"])
@login_required
def get_profile():
    """Edit profile"""
    return render_template("profile.html")


def initialize_profile_change_handler():
    def topup(form):
        value = form.get("value", 0)
        locks[session.get("user_id")] = True
        db.execute("UPDATE users SET cash = cash + :value where id = :id", value=value, id=session.get("user_id"))
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, '_CASH_', 0, :value)",
                   user_id=session.get("user_id"), value=value)
        locks.pop(session.get("user_id"), None)
        flash(f"Successfully added {value} to CASH!")
        return redirect("/")
    def withdraw(form):
        value = form.get("value", 0)
        db.execute("UPDATE users SET cash = cash - :value where id = :id", value=value, id=session.get("user_id"))
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, '_CASH_', 0, :value)",
                   user_id=session.get("user_id"), value=-value)
        flash(f"Successfully withdrew {value} from CASH!")
        return redirect("/")
    def username(form):
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE id = :id",
                          id=session.get("user_id"))[0]

        # Ensure user exists and password is correct
        if not (user and check_password_hash(user["hash"], password)):
            return apology("invalid password", 403)
        db.execute("UPDATE users SET username = :username where id = :id", username=username, id=session.get("user_id"))
        flash(f"Successfully changed username to {username}!")
        return redirect("/")
    def password(form):
        oldPassword = form.get("old-password", None)
        newPassword = form.get("new-password", None)
        confirmation = form.get("confirmation", None)
        if not form.get("old-password"):
            return apology("must provide old password", 403)
        user = db.execute("SELECT * FROM users WHERE id = :id", id=session.get("user_id"))[0]
        if not user or not check_password_hash(user["hash"], form.get("old-password")):
            return apology("invalid old password", 403)
        if not (oldPassword and newPassword and confirmation and newPassword == confirmation):
            return apology("passwords don't match")
        db.execute("UPDATE users SET hash = :hash", hash=generate_password_hash(newPassword))
        flash("Successfully changed password!")
        return redirect("/")
    def deleteUser(form):
        db.execute("DELETE FROM users WHERE id = :id", id=session.get("user_id"))
        db.execute("DELETE FROM transactions WHERE user_id = :id", id=session.get("user_id"))
        session.clear()
        flash(f"Successfully deleted account!")
        return redirect("/")
    return {
        "top-up": topup,
        "withdraw": withdraw,
        "username": username,
        "password": password,
        "delete-user": deleteUser
    }
profile_change_handler = initialize_profile_change_handler()


@app.route("/profile", methods=["POST"])
@login_required
def post_profile():
    """Edit profile"""
    choice = profile_change_handler.get(request.form["type"], False)
    if not choice:
        return apology("invalid form")
    return choice(request.form)


@app.route("/quote", methods=["GET"])
@login_required
def get_quote():
    """Get stock quote."""
    return render_template("quote.html")


@app.route("/quote", methods=["POST"])
@login_required
def post_quote():
    """Get stock quote."""
    symbol = request.form.get("symbol", None)
    if not symbol:
        return apology("missing symbol")
    quote = lookup(symbol)
    if not isinstance(quote, dict):
        return apology("invalid symbol")
    return render_template("quoted.html", quote="A share of {name} ({symbol}) costs {price}.".format(**quote))


@app.route("/register", methods=["GET"])
def get_register():
    """Register user"""
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    """Register user"""

    username = request.form.get("username", None)
    password = request.form.get("password", None)
    confirmation = request.form.get("confirmation", None)
    if not (username and password and confirmation and password == confirmation):
        return apology("passwords don't match")
    if len(db.execute("SELECT id from users WHERE username = :username", username=username)) > 0:
        return apology("username is not available")
    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
               username=username, hash=generate_password_hash(password))
    print(f"username: {username} hash: {generate_password_hash(password)}")

    # Remember which user has logged in
    session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username",
                                    username=username)[0].get("id")

    # Redirect user to home page
    return redirect("/")


@app.route("/sell", methods=["GET"])
@login_required
def get_sell():
    """Sell shares of stock"""
    symbols = sorted({symbol["symbol"] for symbol in db.execute("SELECT symbol FROM transactions WHERE user_id = :id", id=session.get("user_id", ""))})
    return render_template("sell.html", symbols=symbols)


@app.route("/sell", methods=["POST"])
@login_required
def post_sell():
    """Sell shares of stock"""
    symbol = request.form.get("symbol", "")
    if not symbol:
        return apology("missing symbol")
    quote = lookup(symbol)
    if not isinstance(quote, dict):
        return apology("invalid symbol")

    sharesStr = request.form.get("shares", "")
    if not (sharesStr.isdigit() and int(sharesStr) > 0):
        return apology("shares must be a counting number")
    shares = int(sharesStr)

    while locks.get(session.get("user_id"), False):
        pass
    locks[session.get("user_id")] = True
    user = db.execute("SELECT * FROM users WHERE id = :id", id=session.get("user_id"))[0]
    transactions = db.execute("SELECT * FROM transactions WHERE (user_id, symbol) = (:id, :symbol)",
                              id=session.get("user_id"), symbol=symbol)
    totalShares = 0
    for transaction in transactions:
        totalShares += int(transaction.get("shares"))
    if totalShares < shares:
        locks.pop(session.get("user_id"), None)
        return apology("can't afford")
    price = quote.get("price_float")
    totalValue = price * shares
    db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=user.get("cash") + totalValue, id=session.get("user_id"))
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
               user_id=session.get("user_id"), symbol=quote.get("symbol"), shares=-shares, price=price)
    locks.pop(session.get("user_id"), None)
    flash("Sold!")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


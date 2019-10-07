// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// maps a char to an index
int char2index(char c)
{
    if (c == '\'')
    {
        return 26;
    }
    if (c >= 'a' && c <= 'z')
    {
        return c - 'a';
    }
    return c - 'A';
}

node *makeNode()
{
    node *n = malloc(sizeof(node));
    n->is_word = false;
    for (int i = 0; i < N; i++)
    {
        n->children[i] = NULL;
    }
    return n;
}

void destroyNode(node *n)
{
    if (n == NULL)
    {
        return;
    }
    for (int i = 0; i < N; i++)
    {
        destroyNode(n->children[i]);
    }
    free(n);
}

void addWord(node *n, const char *word)
{

    // return if the word is empty
    if (word[0] == '\0')
    {
        n->is_word = true;
        return;
    }

    if (n->children[char2index(word[0])] == NULL)
    {
        n->children[char2index(word[0])] = makeNode();
    }

    addWord(n->children[char2index(word[0])], word + 1);
}

// Represents a trie
node *root;

int wordCount;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    wordCount = 0;

    // Initialize trie
    root = makeNode();
    // root = malloc(sizeof(node));
    // if (root == NULL)
    // {
    //     return false;
    // }
    // root->is_word = false;
    // for (int i = 0; i < N; i++)
    // {
    //     root->children[i] = NULL;
    // }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        addWord(root, word);
        wordCount++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

bool checkBase(node *n, const char *word)
{
    if (n == NULL)
    {
        return false;
    }
    if (word[0] == '\0')
    {
        return n->is_word;
    }
    return checkBase(n->children[char2index(word[0])], word + 1);
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    return checkBase(root, word);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (root == NULL)
    {
        return false;
    }
    destroyNode(root);
    root = NULL;
    wordCount = 0;
    return true;
}

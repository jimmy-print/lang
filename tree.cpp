#include <vector>
#include <iostream>
#include <string>

const std::string DOWN = "DOWN";
const std::string UP = "UP";

class node {
public:
    int v;
    std::vector<node*> child_nodes;
    node* parent;
public:
    node(int vp, node* parentp) {
        v = vp;
        parent = parentp;
    }
    
    void add(node* n) {
        n->parent = this;
        child_nodes.push_back(n);
    }
};

void vis(node* node, int layer)
{
    std::string gap = "";
    for (int i = 0; i < layer; i++) {
        gap += ' ';
    }
    std::cout << gap << node->v << "\n";
    for (auto node : node->child_nodes) {
        if (node != NULL) {
            vis(node, layer + 1);
        }
    }
}

node* index(node* node, std::string dir, std::string i)
{
    if (dir == DOWN) {

    } else if (dir == UP) {

    }
}

int main()
{
    node* root = new node(0, NULL);
    root->add(new node(1, NULL));
    root->add(new node(2, NULL));

    vis(root, 0);
}

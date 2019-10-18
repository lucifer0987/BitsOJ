#include<bits/stdc++.h>
using namespace std;

#define ll long long 

struct Node
{
	int data;
	struct Node *left, *right;
	Node(int data)
	{
		this->data = data;
		left = right = NULL;
	}
};

void printInOrder(struct Node* node)
{
	if(node == NULL)
	{
		return ;
	}
	
	printInOrder(node->left);

	cout << node->data << " ";

	printInOrder(node->right);
}

void printPreorder(struct Node* node)
{
	if(node == NULL)
		return;

	cout << node->data <<" ";

	printPreorder( node->left );

	printPreorder( node->right );

}

void printPostorder(struct Node* node)
{
	if(node == NULL)
		return;

	printPostorder( node->left );

	printPostorder( node->right );

	cout << node->data << " ";
}

int main()
{
	struct Node* root = new Node(1);
	root->left = new Node(2);
	root->right = new Node(3);
	root->left->left = new Node(4);
	root->left->right = new Node(5);

	printInOrder(root);
	cout<<endl;
	printPreorder(root);
	cout<<endl;
	printPostorder(root);
	
}
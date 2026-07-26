#include<iostream>
#include<algorithm>
#include<vector>
using namespace std;

class AVLNode
{
public:
    AVLNode(int k): key(k),height(1),left(nullptr),right(nullptr){}
    int key;
    int height;
    AVLNode* left;
    AVLNode* right;
};

class AVLTree
{
public:
    AVLTree ():root(nullptr){};
    ~AVLTree(){destroy(root);};
    AVLTree(const AVLTree& other):root(copyTree(other.root)){}  //拷贝构造函数
    AVLTree& operator=(const AVLTree other)//赋值运算符重载
    {
        if(this!=&other)
        {
            destroy(root);
            root=copyTree(other.root);
        }
        return *this;
    }
    void insert(int key)
    {
        root=insertNode(root,key);//注意！要加上root=
    }
    void remove(int key)
    {
        root=removeNode(root,key);//注意！要加上root=
    }
    bool search(int key) const
    {
        return searchNode(root,key);
    }
    int getHeight() const
    {
        return height(root);
    }
    bool isEmpty() const
    {
        return root==nullptr;
    }
    vector<int> inorderTraversal() const
    {
        vector<int> arr;
        inorderHelper(root,arr);
        return arr;
    }
    vector<int> preorderTraversal() const
    {
        vector<int> arr;
        preorderHelper(root,arr);
        return arr;
    }
    bool isBalancedTree() const
    {
        return checkBalance(root);
    }
private:
    AVLNode* root;//根节点
    int height(AVLNode* node) const
    {
        if(node==nullptr)
            return 0;
        return node->height;
    }
    int getBalance(AVLNode* node) const
    {
        if(node==nullptr)
            return 0;
        return height(node->left)-height(node->right);
    }
    AVLNode* rightRotation(AVLNode* y)// rotate 本身只关心"局部"，不碰 parent
    {
        AVLNode* x=y->left;
        if (x==nullptr)
            return y;
        y->left=x->right;
        x->right=y;
        y->height=max(height(y->left),height(y->right))+1;
        x->height=max(height(x->left),height(x->right))+1;
        return x;
    }
    AVLNode* leftRotation(AVLNode* x)// rotate 本身只关心"局部"，不碰 parent
    {
        AVLNode* y=x->right;
        if (y==nullptr)
            return x;
        x->right=y->left;
        y->left=x;
        x->height=max(height(x->left),height(x->right))+1;
        y->height=max(height(y->left),height(y->right))+1;
        return y;
    }
    AVLNode* insertNode(AVLNode* node,int key)//递归插入 key，返回重新平衡后的子树根；key 已存在则不做任何修改
    {
        //====第一步====
        //普通BST的插入
        if(node==nullptr)//终止条件
            return new AVLNode(key);

        if(key<node->key)
            node->left=insertNode(node->left,key);
        else if(key>node->key)
            node->right=insertNode(node->right,key);
        else
            return node;  //由AVL树的性质决定      

       // ===== 第二步=====
       // 更新高度
       // 算平衡因子
       // 四种旋转判断
       // ===========================
        node->height=max(height(node->left),height(node->right))+1;
        int balance=getBalance(node);
        if(abs(balance)>1)
        {
            if(balance>0)//一开始以为要右旋
            {
                if(getBalance(node->left)>0)
                {
                    return rightRotation(node);
                }
                else
                {
                    node->left=leftRotation(node->left);
                    return rightRotation(node);
                }
            }
            else         //一开始以为要左旋
            {
                if(getBalance(node->right)<0)
                {
                    return leftRotation(node);
                }
                else
                {
                    node->right=rightRotation(node->right);
                    return leftRotation(node);
                }
            }
        }
        return node;      //很重要
    }

    AVLNode* minValueNode(AVLNode* node) const
    {
        if(node->left==nullptr)
            return node;
        return minValueNode(node->left);
    }

    AVLNode* removeNode(AVLNode* node,int key)
    {
        if(node==nullptr)
            return node;//return nullptr

        if(key<node->key)
            node->left=removeNode(node->left,key);
        else if(key>node->key)
            node->right=removeNode(node->right,key);
        else  
        {
            if(node->left==nullptr)
            {
                AVLNode* temp=node->right;
                delete node;
                return temp;
            }
            else if(node->right==nullptr)
            {
                AVLNode* temp=node->left;
                delete node;
                return temp;
            }
            // 情况3：有两个孩子 —— 不能物理删除，因为无法同时重连两个子树
            // 改为"值替换"策略：用中序后继的 key 覆盖当前节点，
            // 然后递归删除后继（后继最多只有一个孩子，走情况1/2）
            // 注意：这里不 return！让代码继续走到下面的"更新高度+旋转"，
            // 这样删除后继导致的失衡才能被逐层修复
            else
            {
                AVLNode* temp=minValueNode(node->right);     // 中序后继
                node->key=temp->key;                          // 用后继的值覆盖
                node->right=removeNode(node->right,temp->key);// 递归删除后继
            }
        }
        
        node->height=max(height(node->left),height(node->right))+1;
        int balance=getBalance(node);
        if(abs(balance)>1)
        {
            if(balance>0)//一开始以为要右旋
            {
                if(getBalance(node->left)>0)
                {
                    return rightRotation(node);
                }
                else
                {
                    node->left=leftRotation(node->left);
                    return rightRotation(node);
                }
            }
            else         //一开始以为要左旋
            {
                if(getBalance(node->right)<0)
                {
                    return leftRotation(node);
                }
                else
                {
                    node->right=rightRotation(node->right);
                    return leftRotation(node);
                }
            }
        }
        return node;      //很重要 
    }
    bool searchNode(AVLNode* node,int key) const
    {
        if(node==nullptr)
            return false;
        
        if(key<node->key)
            return searchNode(node->left,key);
        else if(key>node->key)
            return searchNode(node->right,key);
        else
            return true;
    }
    void inorderHelper(AVLNode* node,vector<int>& result) const
    {
        if(node==nullptr)
            return;
        inorderHelper(node->left,result);
        result.push_back(node->key);
        inorderHelper(node->right,result);
    }
    void preorderHelper(AVLNode* node,vector<int>& result) const
    {
        if(node==nullptr)
            return;
        result.push_back(node->key);
        preorderHelper(node->left,result);
        preorderHelper(node->right,result);
    }
    void destroy(AVLNode* node)
    {
        if(node==nullptr)
            return;
        destroy(node->left);
        destroy(node->right);
        delete node;
    }
    AVLNode* copyTree(AVLNode* node) const
    {
        if(node==nullptr)
            return nullptr;

        AVLNode* ptr=new AVLNode(node->key);
        ptr->height=node->height;
        ptr->left=copyTree(node->left);
        ptr->right=copyTree(node->right);
        //ptr->height=max(height(ptr->left),height(ptr->right))+1;
        return ptr;
    }
    bool checkBalance(AVLNode* node) const//检查AVL性质（选做）
    {
        int balance=getBalance(node);
        if (node==nullptr)
            return true;
        if(abs(balance)<2)
            return checkBalance(node->left) and checkBalance(node->right);
        else
            return false;
    }
};

void printVec(const vector<int>& v) {
    for (int x : v) cout << x << " ";
    cout << endl;
}

int main() {
    AVLTree tree;

    // 经典插入序列，插入过程中会依次触发 RR、RR、RL 三次旋转
    int keys[] = {10, 20, 30, 40, 50, 25};
    for (int k : keys) tree.insert(k);

    cout << "Height: " << tree.getHeight() << endl;        // 3
    cout << "Preorder: ";
    printVec(tree.preorderTraversal());                     // 30 20 10 25 40 50
    cout << "Inorder: ";
    printVec(tree.inorderTraversal());                       // 10 20 25 30 40 50
    cout << "Balanced? " << tree.isBalancedTree() << endl;  // 1

    cout << "Search 25: " << tree.search(25) << endl;      // 1
    cout << "Search 100: " << tree.search(100) << endl;    // 0

    tree.insert(30);  // 重复插入，树不应发生任何变化
    cout << "After duplicate insert, preorder: ";
    printVec(tree.preorderTraversal());                     // 30 20 10 25 40 50

    tree.remove(40);  // 40 只有一个右孩子 50，删除后不触发旋转
    cout << "After remove(40), preorder: ";
    printVec(tree.preorderTraversal());                     // 30 20 10 25 50
    cout << "Height: " << tree.getHeight() << endl;         // 3

    // 深拷贝验证：拷贝构造后修改原树，副本不应受影响
    AVLTree treeCopy = tree;
    tree.insert(60);
    cout << "Original preorder: ";
    printVec(tree.preorderTraversal());                     // 30 20 10 25 50 60
    cout << "Copy preorder: ";
    printVec(treeCopy.preorderTraversal());                  // 30 20 10 25 50

    // 深拷贝验证：赋值运算符
    AVLTree treeAssigned;
    treeAssigned = tree;
    tree.remove(60);
    cout << "Original after remove(60): ";
    printVec(tree.preorderTraversal());                     // 30 20 10 25 50
    cout << "Assigned copy: ";
    printVec(treeAssigned.preorderTraversal());              // 30 20 10 25 50 60

    // 空树与非法删除的边界测试
    AVLTree emptyTree;
    cout << "isEmpty: " << emptyTree.isEmpty() << endl;      // 1
    emptyTree.remove(5);   // 空树删除，不应崩溃，且不改变任何状态
    cout << "isEmpty after remove on empty: "
         << emptyTree.isEmpty() << endl;                    // 1

    return 0;
}
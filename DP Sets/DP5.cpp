/*
Obert Ratkins 正在一家高档塔帕斯餐吧用餐，并准备点许多小份菜。菜单上共有 \(n\) 道菜，第
 \(i\) 道菜的信息由一个非负整数三元组 \((v_i,c_i,s_i)\) 给出：\(v_i\) 是菜品体积，\(c_i\)
是热量，甜味标记 \(s_i\in\{0,1\}\)（当 \(s_i=1\) 时为甜味菜品，当 \(s_i=0\) 时为非甜味菜品）。
Obert 正在节食：这一餐摄入的热量不能超过 \(k\)，但他又希望尽可能填饱肚子。他还要求恰好点 \(s<n\) 
道甜味菜品，并且同一道菜不能购买两次。请描述一个时间复杂度为 \(O(nks)\) 的算法，在上述饮食限
制下求出 Obert 能吃到的食物最大总体积。
*/

#include<iostream>
#include<vector>
#include<algorithm>
#include<climits>
using namespace std;

int n,k,s;
vector<int> food(3);

int dp(int i,int j,int k,vector<vector<vector<int>>>& memo,const vector<vector<int>>& foods)
{
    if(j<0 or k<0)
        return INT_MIN;
    
    //补丁完成
    if(i==n)
    {
        if(k==0)
            return 0;
        else
            return INT_MIN;
    }

    if(memo[i][j][k]!=-1)            //补丁完成
        return memo[i][j][k];
        
    int s=max(dp(i+1,j,k,memo,foods),dp(i+1,j-foods[i][1],k-foods[i][2],memo,foods)+foods[i][0]);
    memo[i][j][k]=s;
    return s;
}

int main()
{
    cout<<"前情提要:这道题其实本人对于算法和实现思路是比较明确的，但是在编程实现的细节上屡屡翻车，最终大体功能可以实现，但是如果没有可行方案的话，会返回一个很大的负值喵\n";

    cin>>n>>k>>s;

    //补丁完成
    vector<int> arr1(s+1,-1);
    vector<vector<int>> arr2(k+1,arr1);
    vector<vector<vector<int>>> memo(n,arr2);

    vector<vector<int>> foods;

    for(int i=0;i<n;i++)
    {
        int v,c,s;
        cin>>v>>c>>s;
        food[0]=v;
        food[1]=c;
        food[2]=s;
        foods.push_back(food);
    }

    cout<<dp(0,k,s,memo,foods);
    system("pause");
    return 0;
}
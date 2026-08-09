//有趣的保龄球得分最高问题
#include<iostream>
#include<vector>
#include<algorithm>
#include<climits>
using namespace std;

int maxScore(int i,int j,vector<vector<int>>& memo,const vector<int>& score)
{
    if(i>j)
        return 0;

    if(memo[i][j]!=INT_MIN)
        return memo[i][j];

    if(i==j)
    {
        memo[i][i]=max(score[i],0);
        return memo[i][i];
    }
    else
    {
        int record=0;
        for(int k=i;k<=j;k++)
            record=max(record,maxScore(i,k-1,memo,score)+maxScore(k+1,j,memo,score)+score[k]);
        for(int k=i;k<=j-1;k++)
            record=max(record,maxScore(i,k-1,memo,score)+maxScore(k+2,j,memo,score)+score[k]*score[k+1]);
        memo[i][j]=record;
        return record;
    }   
}

int main()
{
    int n;
    cin>>n;
    vector<int> score(n,INT_MIN);
    vector<vector<int>> memo(n,score);

    for(int i=0;i<n;i++)
    {
        cin>>score[i];
        memo[i][i]=max(score[i],0);
    }

    cout<<maxScore(0,n-1,memo,score);
    return 0;
}

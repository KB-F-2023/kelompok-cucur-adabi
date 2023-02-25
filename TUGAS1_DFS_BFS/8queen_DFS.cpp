#include <bits/stdc++.h>
using namespace std;

class QueenPuzzle{
    public:
        class node{
            public:
                node *prev;
                int qp[8];
                int queens;
        };
        int queenPositions[8];
        QueenPuzzle(){
            for(int i=0; i<8; i++){
                queenPositions[i] = -1;
            }
        }

        bool isValid(int qp[8]){
            for(int i=0; i<7; i++){
                for(int j=i+1; j<8; j++){
                    if(qp[j] == -1 || qp[i] == -1){
                        continue;
                    }
                    if(qp[i] == qp[j]){ //cek horizontal
                        return false;
                    }
                    if(abs(qp[i]-qp[j]) == abs(i-j)){ //cek diagonal
                        return false;
                    }
                }
            }
            return true;
        }

        void printStepByStep(node n){
            if(n.prev != NULL){
                printStepByStep(*n.prev);
            }
            printBoard(n);
        }

        void solveDFS(){
            stack<node*> q;
            int nodesCreated = 0;
            node *rootNode = new node;
            rootNode->prev = NULL;
            copy(queenPositions, queenPositions + 8, rootNode->qp);
            rootNode->queens = 0;
            q.push(rootNode);
            while(!q.empty()){
                node *currNode = q.top();
                q.pop();
                if(currNode->queens == 8){
                    cout<<"HASIL DFS:\n";
                    printStepByStep(*currNode);
                    cout<<"nodes created: "<<nodesCreated<<"\n\n";
                    return;
                }
                else{
                    for(int i=0; i<8; i++){
                        node *newNode = new node;
                        *newNode = *currNode;
                        newNode->qp[newNode->queens] = i;
                        if(isValid(newNode->qp)){
                            newNode->prev = currNode;
                            newNode->queens = newNode->queens + 1;
                            nodesCreated++;
                            q.push(newNode);
                        }
                    }
                }
            }
        }

        void printBoard(node n){
            bool board[8][8];
            for(int i=0;i<8;i++){
                for(int j=0;j<8;j++){
                    board[i][j]=false;
                }
            }
            for(int i=0;i<8;i++){
                board[n.qp[i]][i] = true;
            }
            for(int i=0;i<8;i++){
                for(int j=0;j<8;j++){
                    cout<<board[i][j]<<" ";
                }
                cout<<endl;
            }
            cout<<endl;
        }

        void printqp(){
            for(int i=0;i<8;i++){
                cout<<queenPositions[i]<<" ";
            }
            cout<<endl;
        }

        void printqp(node n){
            for(int i=0;i<8;i++){
                cout<<n.qp[i]<<" ";
            }
            cout<<endl;
        }
};

int main(){
    QueenPuzzle dfsSolution;
    dfsSolution.solveDFS();
}
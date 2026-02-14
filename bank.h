#include <iostream>
#include <string>
using namespace std;

class Account {
private:
    int bal=0;
public:
//      void setBalance(int b) { 
//         bal = b;
//         }
//     int getBalance() {
//         return bal;
//         }

    void deposit() {
        int amt;
        cout << "Enter amount to deposit: ";
        cin >> amt;
        if(amt>0){
        bal += amt;
        cout << "\nTransaction Successful: Deposit" << endl;
        displayTransaction("Deposit", amt);
        }
        else{
            cout << "\nInvalid Amount";
        }
    }

    void withdraw() {
        int amt;
        cout << "Enter amount to withdraw: ";
        cin >> amt;
        if (amt <= bal && amt>0) {
            bal -= amt;
            cout << "\nTransaction Successful: Withdrawal" << endl;
            displayTransaction("Withdrawal", amt);
        } else {
            cout << "\nTransaction Failed: Insufficient Balance" << endl;
        }
    }

    void displayTransaction(string type, int amount) {
        cout << "\nTransaction Type: " << type << endl;
        cout << "Transaction Amount: " << amount << endl;
        cout << "Updated Balance: " << bal << endl;
    }
};

class Customer {
private:
    int cid;
    string cname;
    string cadd;
    int acno;
    Account acc;  

public:
    void setData() {
        // int bal;
        cout << "Enter customer ID: ";
        cin >> cid;
        cout << "Enter customer name: ";
        cin >> cname;
        cout << "Enter customer address: ";
        cin >> cadd;
        cout << "Enter account no: ";
        cin >> acno;
        // cout << "Enter balance: ";
        // cin >> bal;
        // acc.setBalance(bal);
    }

    void getData() {
        cout << "\n--- Customer Details ---" << endl;
        cout << "Customer ID: " << cid << endl;
        cout << "Customer Name: " << cname << endl;
        cout << "Customer Address: " << cadd << endl;
        cout << "Account No: " << acno << endl;
        // cout << "Balance: " << acc.getBalance() << endl;
    }

    void menu() {
        int choice;
        do {
            cout << "\n1. Deposit\n2. Withdraw\n3. Exit\nEnter choice: ";
            cin >> choice;

            switch (choice) {
                case 1: acc.deposit(); break;
                case 2: acc.withdraw(); break;
                case 3: cout << "Exiting..." << endl; break;
                default: cout << "Invalid choice!" << endl;
            }
        } while (choice != 3);
    }
};

int main() {
    Customer c;
    c.setData();
    c.getData();
    c.menu();   
    return 0;
}


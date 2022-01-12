
    printf("|%c    |\n", diamond);
    printf("|  J  |\n");
    printf("|    %c|\n", diamond);
    printf("-------\n");
    }
     
    if(k==11) //If random number is 11, print card with A (Ace) on face
    {
    //Diamond Card
    printf("-------\n");
    printf("|%c    |\n", diamond);
    printf("|  A  |\n");
    printf("|    %c|\n", diamond);
    printf("-------\n");
    if(player_total<=10) //If random number is Ace, change value to 11 or 1 depending on dealer total
         {
             k=11;
         }
          
         else
         {
             k=1;
         }
    }
     
    if(k==12) //If random number is 12, print card with Q (Queen) on face
    {
    //Diamond Card
    printf("-------\n");
    printf("|%c    |\n", diamond);
    printf("|  Q  |\n");
    printf("|    %c|\n", diamond);
    printf("-------\n");
    k=10; //Set card value to 10
    }
     
    if(k==13) //If random number is 13, print card with K (King) on face
    {
    //Diamond Card
    printf("-------\n");
    printf("|%c    |\n", diamond);
    printf("|  K  |\n");
    printf("|    %c|\n", diamond);
    printf("-------\n");
    k=10; //Set card value to 10
    }
    return k;
}// End function
 
int heartcard() //Displays Heart Card Image
{
     
     
    srand((unsigned) time(NULL)); //Generates random seed for rand() function
    k=rand()%13+1;
     
    if(k<=9) //If random number is 9 or less, print card with that number
    {
    //Heart Card
    printf("-------\n");
    printf("|%c    |\n", heart); 
    printf("|  %d  |\n", k);
    printf("|    %c|\n", heart);
    printf("-------\n");
    }
     
    if(k==10) //If random number is 10, print card with J (Jack) on face
    {
    //Heart Card
    printf("-------\n");
    printf("|%c    |\n", heart);
    printf("|  J  |\n");
    printf("|    %c|\n", heart);
    printf("-------\n");
    }
     
    if(k==11) //If random number is 11, print card with A (Ace) on face
    {
    //Heart Card
    printf("-------\n");
    printf("|%c    |\n", heart);
    printf("|  A  |\n");
    printf("|    %c|\n", heart);
    printf("-------\n");
    if(player_total<=10) //If random number is Ace, change value to 11 or 1 depending on dealer total
         {
             k=11;
         }
          
         else
         {
             k=1;
         }
    }
     
    if(k==12) //If random number is 12, print card with Q (Queen) on face
    {
    //Heart Card
    printf("-------\n");
    printf("|%c    |\n", heart);
    printf("|  Q  |\n");
    printf("|    %c|\n", heart);
    printf("-------\n");
    k=10; //Set card value to 10
    }
     
    if(k==13) //If random number is 13, print card with K (King) on face
    {
    //Heart Card
    printf("-------\n");
    printf("|%c    |\n", heart);
    printf("|  K  |\n");
    printf("|    %c|\n", heart);
    printf("-------\n");
    k=10; //Set card value to 10
    }
    return k;
} // End Function
 
int spadecard() //Displays Spade Card Image
{
     
     
    srand((unsigned) time(NULL)); //Generates random seed for rand() function
    k=rand()%13+1;
     
    if(k<=9) //If random number is 9 or less, print card with that number
    {
    //Spade Card
    printf("-------\n");
    printf("|%c    |\n", spade);
    printf("|  %d  |\n", k);
    printf("|    %c|\n", spade);
    printf("-------\n");
    }
     
    if(k==10) //If random number is 10, print card with J (Jack) on face
    {
    //Spade Card
    printf("-------\n");
    printf("|%c    |\n", spade);
    printf("|  J  |\n");
    printf("|    %c|\n", spade);
    printf("-------\n");
    }
     
    if(k==11) //If random number is 11, print card with A (Ace) on face
    {
    //Spade Card
    printf("-------\n");
    printf("|%c    |\n", spade);
    printf("|  A  |\n");
    printf("|    %c|\n", spade);
    printf("-------\n");
    if(player_total<=10) //If random number is Ace, change value to 11 or 1 depending on dealer total
         {
             k=11;
         }
          
         else
         {
             k=1;
         }
    }
     
    if(k==12) //If random number is 12, print card with Q (Queen) on face
    {
    //Spade Card
    printf("-------\n");
    printf("|%c    |\n", spade);
    printf("|  Q  |\n");
    printf("|    %c|\n", spade);
    printf("-------\n");
    k=10; //Set card value to 10
    }
     
    if(k==13) //If random number is 13, print card with K (King) on face
    {
    //Spade Card
    printf("-------\n");
    printf("|%c    |\n", spade);
    printf("|  K  |\n");
    printf("|    %c|\n", spade);
    printf("-------\n");
    k=10; //Set card value to 10
    }
    return k;
} // End Function
 
int randcard() //Generates random card
{
      
                
     srand((unsigned) time(NULL)); //Generates random seed for rand() function
     random_card = rand()%4+1;
      
     if(random_card==1)
     {   
         clubcard();
         l=k;
     }
      
     if(random_card==2)
     {
         diamondcard();
         l=k;
     }
      
     if(random_card==3)
     {
         heartcard();
         l=k;
     }
          
     if(random_card==4)
     {
         spadecard();
         l=k;
     }    
     return l;
} // End Function   
 
void play() //Plays game
{
      
     int p=0; // holds value of player_total
     int i=1; // counter for asking user to hold or stay (aka game turns)
     char choice3;
      
     cash = cash;
     cash_test();
     printf("\nCash: $%d\n",cash); //Prints amount of cash user has
     randcard(); //Generates random card
     player_total = p + l; //Computes player total
     p = player_total;
     printf("\nYour Total is %d\n", p); //Prints player total
     dealer(); //Computes and prints dealer total
     betting(); //Prompts user to enter bet amount
        
     while(i<=21) //While loop used to keep asking user to hit or stay at most twenty-one times
                  //  because there is a chance user can generate twenty-one consecutive 1's
     {
         if(p==21) //If user total is 21, win
         {
             printf("\nUnbelievable! You Win!\n");
             won = won+1;
             cash = cash+bet;
             printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
             dealer_total=0;
             askover();
         }
      
         if(p>21) //If player total is over 21, loss
         {
             printf("\nWoah Buddy, You Went WAY over.\n");
             loss = loss+1;
             cash = cash - bet;
             printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
             dealer_total=0;
             askover();
         }
      
         if(p<=21) //If player total is less than 21, ask to hit or stay
         {         
             printf("\n\nWould You Like to Hit or Stay?");
              
             scanf("%c", &choice3);
             while((choice3!='H') && (choice3!='h') && (choice3!='S') && (choice3!='s')) // If invalid choice entered
             {                                                                           
                 printf("\n");
                 printf("Please Enter H to Hit or S to Stay.\n");
                 scanf("%c",&choice3);
             }
 
 
             if((choice3=='H') || (choice3=='h')) // If Hit, continues
             { 
                 randcard();
                 player_total = p + l;
                 p = player_total;
                 printf("\nYour Total is %d\n", p);
                 dealer();
                  if(dealer_total==21) //Is dealer total is 21, loss
                  {
                      printf("\nDealer Has the Better Hand. You Lose.\n");
                      loss = loss+1;
                      cash = cash - bet;
                      printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
                      dealer_total=0;
                      askover();
                  } 
      
                  if(dealer_total>21) //If dealer total is over 21, win
                  {                      
                      printf("\nDealer Has Went Over!. You Win!\n");
                      won = won+1;
                      cash = cash+bet;
                      printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
                      dealer_total=0;
                      askover();
                  }
             }
             if((choice3=='S') || (choice3=='s')) // If Stay, does not continue
             {
                printf("\nYou Have Chosen to Stay at %d. Wise Decision!\n", player_total);
                stay();
             }
          }
             i++; //While player total and dealer total are less than 21, re-do while loop 
     } // End While Loop
} // End Function
 
void dealer() //Function to play for dealer AI
{
     int z;
      
     if(dealer_total<17)
     {
      srand((unsigned) time(NULL) + 1); //Generates random seed for rand() function
      z=rand()%13+1;
      if(z<=10) //If random number generated is 10 or less, keep that value
      {
         d=z;
          
      }
      
      if(z>11) //If random number generated is more than 11, change value to 10
      {
         d=10;
      }
      
      if(z==11) //If random number is 11(Ace), change value to 11 or 1 depending on dealer total
      {
         if(dealer_total<=10)
         {
             d=11;
         }
          
         else
         {
             d=1;
         }
      }
     dealer_total = dealer_total + d;
     }
           
     printf("\nThe Dealer Has a Total of %d", dealer_total); //Prints dealer total
      
} // End Function 
 
void stay() //Function for when user selects 'Stay'
{
     dealer(); //If stay selected, dealer continues going
     if(dealer_total>=17)
     {
      if(player_total>=dealer_total) //If player's total is more than dealer's total, win
      {
         printf("\nUnbelievable! You Win!\n");
         won = won+1;
         cash = cash+bet;
         printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
         dealer_total=0;
         askover();
      }
      if(player_total<dealer_total) //If player's total is less than dealer's total, loss
      {
         printf("\nDealer Has the Better Hand. You Lose.\n");
         loss = loss+1;
         cash = cash - bet;
         printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
         dealer_total=0;
         askover();
      }
      if(dealer_total>21) //If dealer's total is more than 21, win
      {
         printf("\nUnbelievable! You Win!\n");
         won = won+1;
         cash = cash+bet;
         printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
         dealer_total=0;
         askover();
      }
     }
     else
     {
         stay();
     }
      
} // End Function
 
void cash_test() //Test for if user has cash remaining in purse
{
     if (cash <= 0) //Once user has zero remaining cash, game ends and prompts user to play again
     {
        printf("You Are Bankrupt. Game Over");
        cash = 500;
        askover();
     }
} // End Function
 
int betting() //Asks user amount to bet
{
 printf("\n\nEnter Bet: $");
 scanf("%d", &bet);
 
 if (bet > cash) //If player tries to bet more money than player has
 {
        printf("\nYou cannot bet more money than you have.");
        printf("\nEnter Bet: ");
        scanf("%d", &bet);
        return bet;
 }
 else return bet;
} // End Function
 
void askover() // Function for asking player if they want to play again
{
    char choice1;
         
     printf("\nWould You Like To Play Again?");
     printf("\nPlease Enter Y for Yes or N for No\n");
     scanf("\n%c",&choice1);
 
    while((choice1!='Y') && (choice1!='y') && (choice1!='N') && (choice1!='n')) // If invalid choice entered
    {                                                                           
        printf("\n");
        printf("Incorrect Choice. Please Enter Y for Yes or N for No.\n");
        scanf("%c",&choice1);
    }
 
 
    if((choice1 == 'Y') || (choice1 == 'y')) // If yes, continue.
    { 
            system("cls");
            play();
    }
  
    else if((choice1 == 'N') || (choice1 == 'n')) // If no, exit program
    {
        fileresults();
        printf("\nBYE!!!!\n\n");
        system("pause");
        exit(0);
    }
    return;
} // End function
 
void fileresults() //Prints results into Blackjack.txt file in program directory
{
    FILE *fpresults; //File pointer is fpresults
    fpresults = fopen(RESULTS, "w"); //Creates file and writes into it
    if(fpresults == NULL) // what to do if file missing from directory
    {
               printf("\nError: File Missing\n");
               system("pause");
               exit(1);
    }
    else
    {     
     fprintf(fpresults,"\n\t RESULTS");
     fprintf(fpresults,"\n\t---------\n");
     fprintf(fpresults,"\nYou Have Won %d Times\n", won);
     fprintf(fpresults,"\nYou Have Lost %d Times\n", loss);
     fprintf(fpresults,"\nKeep Playing and Set an All-Time Record!");
    } 
     fclose(fpresults);
     return;
} // End Function
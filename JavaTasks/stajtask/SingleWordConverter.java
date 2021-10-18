/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package stajtask;

import java.util.Arrays;

/**
 *
 * @author amacemirhan
 */
public class SingleWordConverter {
    public static void removeDuplicate(String[] words){
    String wordsWithRepetition[] = new String[words.length];
    int wrc=1;    //Variable for getting Repeated word count
      
      for(int i=0;i<words.length;i++) //Outer loop for Comparison       
      {
         for(int j=i+1;j<words.length;j++) //Inner loop for Comparison
         {
            
         if(words[i].equals(words[j]))  //Checking for both strings are equal
            {
               wrc=wrc+1;    //if equal increment the count
               words[j]="0"; //Replace repeated words by zero
            }
         }
         if(words[i]!="0")
         wordsWithRepetition[i] = words[i]+" "+wrc; //Printing the word along with count in string
         wrc=1;
         
        } 
    for(int k=0;k<words.length;k++){
        if(words[k]!="0")
        System.out.print(words[k]+" ");
    }
        System.out.println("\n"+"****************");
    for(int k=0;k<wordsWithRepetition.length;k++){
        if(wordsWithRepetition[k]!=null){
        wordsWithRepetition[k] = wordsWithRepetition[k].replace("\n","");
        System.out.println(wordsWithRepetition[k]);
        }
    }
    }
    public static void singleWordConverter(){
    String str ="Happy hour hour class class classs\n " +
    "Do you you go go go go to the the gym\n " +
    "Okey okey bro Bro"; 
        str = str.toLowerCase();
        String words[] = str.split(" ");
        removeDuplicate(words);
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        singleWordConverter();
        
        
        }
    }
    


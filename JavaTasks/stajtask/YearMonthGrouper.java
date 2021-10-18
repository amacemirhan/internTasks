package stajtask;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.Random;
/**
 *
 * @author amacemirhan
 */
public class YearMonthGrouper {
    
    public static void randomDateGenerator(long currentMillis,int dateSample){
    ArrayList<Date> myList = new ArrayList<Date>();
    Random r= new Random();
    long twoYearsToMillis = 63113904000L;//two years in milliseconds
    
        for (int i = 0; i < dateSample; i++) {
            long a = r.nextLong()%twoYearsToMillis;//random duration up to 2 years maximum but can also give us negative (Abs in line 22)
            Date myDate= new Date(currentMillis-Math.abs(a));//Date creation between now-2 years ago
            myList.add(myDate);
        }
        Collections.sort(myList);//Date Sorting before to after
        yearMonthGrouper(myList);
    }
    public static void yearMonthGrouper(ArrayList<Date> myList ){
    LinkedHashMap<String, Integer> dateList = new LinkedHashMap<String, Integer>();//Allows printing in order of insertion (in line 52) thanks to LinkedHashMap
    String formatted[] = new String[myList.size()];
    SimpleDateFormat timeFormat = new SimpleDateFormat("MMM-yy");
        
        for (int i = 0; i < myList.size(); i++) {
            formatted[i]=timeFormat.format(myList.get(i)).toString();// Formatting Date to String
            System.out.println(formatted[i]);
        }
        int n=1;// number of repetitions
        for (int i = 0; i < formatted.length; i++) {
            if(formatted[i]=="0")
                continue;
            for (int j = i+1; j < formatted.length; j++) {
                if(formatted[i].equals(formatted[j])){
                n = n+1;
                formatted[j]="0";//eliminate of same dates with line 39
                }
            }
            dateList.put(formatted[i], n);
            n=1;
            
        }
        
        System.out.println(dateList);
    }
    public static void main(String[] args) {
        long currentMillis = System.currentTimeMillis();//get system time in milliseconds
        int dateSample=20;// number of date samples
        randomDateGenerator(currentMillis,dateSample);
        }
    
}

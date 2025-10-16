    package com.example.myapplication2;

    import androidx.appcompat.app.AppCompatActivity;
    import androidx.core.app.ActivityCompat;
    import androidx.core.content.ContextCompat;
    import android.telephony.SmsManager;

    import android.Manifest;
    import android.app.PendingIntent;
    import android.content.Context;
    import android.content.Intent;
    import android.content.IntentFilter;
    import android.content.pm.PackageManager;
    import android.nfc.NdefMessage;
    import android.nfc.NdefRecord;
    import android.nfc.NfcAdapter;
    import android.nfc.Tag;
    import android.os.AsyncTask;
    import android.os.Bundle;
    import android.os.Parcelable;
    import android.util.Log;
    import android.view.View;
    import android.widget.ArrayAdapter;
    import android.widget.Button;
    import android.widget.ImageButton;
    import android.widget.Spinner;
    import android.widget.TextView;
    import android.widget.Toast;

    import java.io.UnsupportedEncodingException;
    import java.sql.Connection;
    import java.sql.DriverManager;
    import java.sql.ResultSet;
    import java.sql.Statement;
    import java.util.ArrayList;
    import java.util.List;

    import com.example.myapplication2.ui.main.MainFragment;

    public class MainActivity extends AppCompatActivity {

        PendingIntent pendingIntent;
        IntentFilter[] intentFilter;
    //    boolean writeMode;
        Tag myTag;
        Context context;

        private static final int REQUEST_SEND_SMS = 1;
    
        public static final String url = "jdbc:mysql://192.168.76.189:3306/safarcard";
        public static final String user = "root";
        public static final String pass = "5877";


        public static final String Stop_Error="Select Bus Stops";
        public static final String Route_Error="Select Bus Route";
        public static final String Balance_Error="Insufficient Balance";
        public static final String Ticket_Generated="Ticket Generated Successfully";
        public static final String Balance_Low=" Ticket Generated Successfully   Warning: User's Balance is Low";

        public static String[][] curr_route=new String[100][2];
        public static int fare=-1;
        public static String curr_userID="";



        TextView textView6;
        Spinner spinner, spinner2, spinner3;
        Button button;
        ImageButton imgButton;

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
            if (savedInstanceState == null) {
                getSupportFragmentManager().beginTransaction()
                        .replace(R.id.container, MainFragment.newInstance())
                        .commitNow();
            }
            NfcAdapter nfcAdapter = NfcAdapter.getDefaultAdapter(this);

            textView6=findViewById(R.id.textView6);
            spinner=findViewById(R.id.spinner);
            spinner2=findViewById(R.id.spinner2);
            spinner3=findViewById(R.id.spinner3);
            button=findViewById(R.id.button);
            imgButton=findViewById(R.id.imageButton);

            readfromIntent(getIntent());
            pendingIntent=PendingIntent.getActivity(this, 0, new Intent(this, getClass()).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP), PendingIntent.FLAG_IMMUTABLE);
            IntentFilter tagDetected=new IntentFilter(NfcAdapter.ACTION_TAG_DISCOVERED);
            tagDetected.addCategory(Intent.CATEGORY_DEFAULT);
            intentFilter=new IntentFilter[]{tagDetected};

            try {
                FetchBusRoutes fetchRoute = new FetchBusRoutes();
                fetchRoute.execute("");
                String[] routes=fetchRoute.get();
                List list= new ArrayList<>();
                list.add("");
                for(int a=0; a<1000;a++) {
                    if (routes[a] == null) {
                        break;
                    }
                    list.add(routes[a]);
                }
                ArrayAdapter<String> adp1 = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, list);
                adp1.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                spinner.setAdapter(adp1);

            } catch (Exception e) {
                e.printStackTrace();
            }

            ArrayAdapter<String> adp2 = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1);
            ArrayAdapter<String> adp3 = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1);


            imgButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String routeno = spinner.getSelectedItem().toString();
                    if (routeno == "") {
                        Toast.makeText(getApplicationContext(), Route_Error, Toast.LENGTH_SHORT).show();
                    } else {
                        try {
                            routeno = routeno.substring(routeno.indexOf("-") + 1);
                            FetchStops stops = new FetchStops();
                            stops.execute(routeno);
                            curr_route = stops.get();
                            List list2 = new ArrayList<>();
                            list2.add("");
                            for (int a = 0; a < 1000; a++) {
                                if (curr_route[a][0] == null) {
                                    break;
                                }
                                list2.add(curr_route[a][0]);
                            }

                            adp2.clear();
                            adp2.notifyDataSetChanged();
                            adp2.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                            adp2.addAll(list2);
                            spinner2.setAdapter(adp2);

                            adp3.clear();
                            adp3.notifyDataSetChanged();
                            adp3.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                            adp3.addAll(list2);
                            spinner3.setAdapter(adp3);

                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            });

            button.setOnClickListener(new View.OnClickListener(){
                public void onClick(View v){
                    try {
                        String stop1 = spinner2.getSelectedItem().toString();
                        String stop2 = spinner3.getSelectedItem().toString();

                        if (stop1 == "" || stop2 == "") {
                            Toast.makeText(getApplicationContext(), Stop_Error, Toast.LENGTH_SHORT).show();
                        } else {
                            int f1 = 0, f2 = 0;

                            for (int i = 0; i < 100; i++) {
                                if (curr_route[i][0] == stop1) {
                                    f1 = Integer.parseInt(curr_route[i][1]);
                                }
                                if (curr_route[i][0] == stop2) {
                                    f2 = Integer.parseInt(curr_route[i][1]);
                                }
                            }
                            if (f2-f1==0)
                                fare = 5;
                            else
                                fare = f2 - f1;
                            if(fare<0)
                                fare=-(fare);
                            textView6.setText("Fare: ₹"+fare);
                        }
                    }
                    catch(Exception e){e.printStackTrace();}
                }
            });
            context=this;
            checkSmsPermission();

        }

        private void checkSmsPermission() {
            // Check if the app has permission to send SMS
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS) != PackageManager.PERMISSION_GRANTED) {
                // Request permission
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.SEND_SMS}, REQUEST_SEND_SMS);
            } else {
                // Permission already granted, proceed with sending SMS
            }
        }

        @Override
        public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
            super.onRequestPermissionsResult(requestCode, permissions, grantResults);
            if (requestCode == REQUEST_SEND_SMS) {
                // Check if permission is granted
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // Permission granted, proceed with sending SMS
                } else {
                    // Permission denied, inform the user or handle the denial gracefully
                    Toast.makeText(this, "SMS permission denied", Toast.LENGTH_SHORT).show();
                }
            }
        }

        private void smsSender(String stop1, String stop2, String remainingBalance, int deductCase, String phoneNumber) {
            try {
                String message = "";

                // Construct message based on deduction case
                switch (deductCase) {
                    case 1:
                        message = String.format("Your ticket has been generated. Remaining balance is: Rs. %s. Have a safe and happy journey.", remainingBalance);
                        break;
                    case 2:
                        message = String.format("Your ticket has been generated. Remaining balance is: Rs. %s. Your balance has gone under 0, please recharge at the earliest.", remainingBalance);
                        break;
                    default:
                        message = String.format("Your ticket could not be generated. Remaining balance is: Rs. %s. Please recharge your SafarCard to continue travelling.", remainingBalance);
                        break;
                }

                Log.d("SMSDebug", "Attempting to send sms to " + phoneNumber);
                Log.d("SMSDebug", "Message is: " + message);

                // Send SMS
                SmsManager smsManager = SmsManager.getDefault();
                smsManager.sendTextMessage(phoneNumber, null, message, null, null);

                Log.d("SMSDebug", "SMS Sending attempted.");

            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        public void readfromIntent(Intent intent) {
            String action=intent.getAction();


                Parcelable[] raw=intent.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES);
                NdefMessage[] msgs=null;
                if(raw!=null){
                    msgs=new NdefMessage[raw.length];
                    for(int i=0; i< raw.length; i++)
                        msgs[i]=(NdefMessage) raw[i];
                }
                buildTagViews(msgs);
            }


            private void buildTagViews (NdefMessage[] msgs) {

                if (msgs == null || msgs.length == 0) return;

                String text ="";
                byte[] payload= msgs[0].getRecords()[0].getPayload();
                String textEncoding = ((payload [0] & 128)==0) ? "UTF-8" : "UTF-16";
                int languageCodeLength = payload [0] & 0063;

                try{
                    text=new String(payload, languageCodeLength+1, payload.length-languageCodeLength-1, textEncoding);
                    Log.v("NFCData", ""+text);
                } catch (UnsupportedEncodingException e) {
                    Log.e("UnsupportedEncoding", e.toString());
                }
                curr_userID=text;
                deduct();
            }

            private NdefRecord createRecord(String text) throws UnsupportedEncodingException{
                String lang="en";
                byte[] textBytes=text.getBytes();
                byte[] langBytes=text.getBytes("US-ASCII");
                int langLen=langBytes.length;
                int textLen=textBytes.length;
                byte[] payload=new byte[1+langLen+textLen];

                payload[0]=(byte) langLen;

                System.arraycopy(langBytes, 0, payload, 1, langLen);
                System.arraycopy(textBytes, 0, payload, 1+langLen, textLen);

                NdefRecord recorfNFC=new NdefRecord(NdefRecord.TNF_WELL_KNOWN, NdefRecord.RTD_TEXT, new byte[0], payload);
                return recorfNFC;
            }

            protected void onNewIntent(Intent intent) {
                super.onNewIntent(intent);
                setIntent(intent);
                readfromIntent(intent);
                if(NfcAdapter.ACTION_TAG_DISCOVERED.equals(intent.getAction())){
                    myTag=intent.getParcelableExtra(NfcAdapter.EXTRA_TAG);
                }
            }

        protected void onPause() {
            super.onPause();
           // WriteModeOff();
        }

        protected void onResume() {
            super.onResume();
          //  WriteModeOn();
        }



        public void deduct(){
            if(fare==-1)
            {
                Toast.makeText(getApplicationContext(), Stop_Error, Toast.LENGTH_SHORT).show();
            }
            else{
                String[] cardno=curr_userID.split(" ",4);
                curr_userID="";
                for(int a=0;a<4;a++)
                    curr_userID+=cardno[a];
                DeductFare deductFare = new DeductFare();
                deductFare.execute("");

                GetRemainingBalance remBal = new GetRemainingBalance();
                remBal.execute("");

                GetPhNo getNumber = new GetPhNo();
                getNumber.execute("");

                String stop1 = spinner2.getSelectedItem().toString();
                String stop2 = spinner3.getSelectedItem().toString();

                try {
                    Integer res=deductFare.get();
                    String number=getNumber.get();
                    Integer remainingBalance=remBal.get();
                    if(res==1){
                        Toast.makeText(getApplicationContext(), Ticket_Generated, Toast.LENGTH_SHORT).show();
                    }
                    else if(res==2)
                    {
                        Toast.makeText(getApplicationContext(), Balance_Low, Toast.LENGTH_SHORT).show();
                    }
                    else {
                        Toast.makeText(getApplicationContext(), Balance_Error, Toast.LENGTH_SHORT).show();
                    }
                    smsSender(stop1, stop2, Integer.toString(remainingBalance), res, number);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }


//        private void smsSender(String stop1, String stop2, String remainingBalance, int deductCase, String phoneNumber){
//            try{
//
//                String message="";
//
//                switch (deductCase) {
//                    case 1:
//                        message= String.format("Your ticket has been generated. Remaining balance is: ₹%s. We wish you a safe and happy journey.", remainingBalance);
//                        break;
//                    case 2:
//                        message= String.format("Your ticket has been generated. Remaining balance is: ₹%s. Your balance has gone under 0, please recharge at the earliest.", remainingBalance);
//                        break;
//                    default:
//                        message= String.format("Your ticket could not be generated due to insufficient balance. Remaining balance is: ₹%s. Please recharge your SafarCard to continue using it.", remainingBalance);
//                        break;
//                }
//
//                System.out.println("Attempting to send sms to "+phoneNumber);
//                System.out.println("Message is: "+message);
//                SmsManager smsManager = SmsManager.getDefault();
//                smsManager.sendTextMessage(phoneNumber, null, message, null, null);
//                System.out.println("SMS Sending attempted.");
//
//            }catch (Exception e){
//                e.printStackTrace();
//            }
//        }




    class FetchBusRoutes extends AsyncTask<String, Void, String[]> {
        String[] res=new String[1000];

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String[] doInBackground(String... params) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
                Connection con = DriverManager.getConnection(url, user, pass);
                System.out.println("Database connection success");

                String result="";
                Statement st = con.createStatement();
                ResultSet rs = st.executeQuery("select * from add_bus;");

                for(int a=0; rs.next(); a++){
                    result=rs.getString(1)+"-"+rs.getString(2);
                    res[a]=result;
                }


            } catch (Exception e) {
                e.printStackTrace();
            }
            return res;
        }

        @Override
        protected void onPostExecute(String[] result) {
            System.out.println(result);
        }
    }




    class FetchStops extends AsyncTask<String, Void, String[][]> {
        String[][] res=new String[1000][2];

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String[][] doInBackground(String... params) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
                Connection con = DriverManager.getConnection(url, user, pass);
                System.out.println("Database connection success");

                String route=params[0];
                Statement st = con.createStatement();
                ResultSet rs = st.executeQuery("select * from "+route+";");

                for(int a=0; rs.next(); a++){
                    res[a][0]=rs.getString(1);
                    res[a][1]=rs.getString(2);
                }


            } catch (Exception e) {
                e.printStackTrace();
            }
            return res;
        }

        @Override
        protected void onPostExecute(String[][] result) {
            System.out.println(result);
        }
    }




    class DeductFare extends AsyncTask<String, Void, Integer> {
        Integer res=1;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();

        }

        @Override
        protected Integer doInBackground(String... params) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
                Connection con = DriverManager.getConnection(url, user, pass);
                System.out.println("Database connection success");

                String route=params[0];
                Statement st = con.createStatement();

                ResultSet rs=st.executeQuery(String.format("SELECT * FROM `user` WHERE (`cardno`='%s');", curr_userID));
                rs.next();
                int balance=rs.getInt(6);

                if(balance-fare<-50){
                    res=0;
                }
                else if(balance-fare<0)
                {
                    res=2;
                    int rs2 = st.executeUpdate(String.format("UPDATE `user` SET `balance` = '%d' WHERE (`cardno` = '%s');", balance-fare, curr_userID));
                }
                else {
                    int rs2 = st.executeUpdate(String.format("UPDATE `user` SET `balance` = '%d' WHERE (`cardno` = '%s');", balance-fare, curr_userID));
                }

            } catch (Exception e) {
                e.printStackTrace();
            }
            return res;
        }

        @Override
        protected void onPostExecute(Integer result) {
            System.out.println(result);
        }
    }



    class GetRemainingBalance extends AsyncTask<String, Void, Integer> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();

        }

        @Override
        protected Integer doInBackground(String... params) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
                Connection con = DriverManager.getConnection(url, user, pass);
                System.out.println("Database connection success");

                String route=params[0];
                Statement st = con.createStatement();

                ResultSet rs=st.executeQuery(String.format("SELECT * FROM `user` WHERE (`cardno`='%s');", curr_userID));
                rs.next();
                int balance=rs.getInt(6);
                return balance;

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Integer result) {
            System.out.println(result);
        }
    }



    class GetPhNo extends AsyncTask<String, Void, String> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String doInBackground(String... params) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
                Connection con = DriverManager.getConnection(url, user, pass);
                System.out.println("Database connection success");

                String route=params[0];
                Statement st = con.createStatement();

                ResultSet rs=st.executeQuery(String.format("SELECT * FROM `user` WHERE (`cardno`='%s');", curr_userID));
                rs.next();
                String balance=rs.getString("phno");
                return balance;

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    }
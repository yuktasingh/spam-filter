package com.example.user.sampleapp;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity {

    private String TAG = MainActivity.class.getSimpleName();
    private ListView lv;

    ArrayList<HashMap<String, String>> contactList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button searchButton;
        final EditText dataEntered;
        searchButton=(Button)findViewById(R.id.searchButton);
        dataEntered=(EditText)findViewById(R.id.dataEntered);
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View vw) {
                String toSearch=dataEntered.getText().toString();
                try {
                    new GetResult(toSearch).execute();

                } catch (Exception e) {

                    Log.i("one",e.toString());
                }

            }
        });
    }

    private class GetResult extends AsyncTask<Void, Void, Void> {
        String message;
        protected GetResult(String mes)
        {
            message=mes;
        }
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected Void doInBackground(Void... arg0) {
            HttpHandler sh = new HttpHandler();
            // Making a request to url and getting response
            String url = "http://192.168.43.147:5000/smish?message="+message;
            String jsonStr = sh.makeServiceCall(url);

            Log.e(TAG, "Response from url: " + jsonStr);
            if (jsonStr != null) {
                Log.i("one",jsonStr);
                TextView textToDisplay;
                textToDisplay=(TextView)findViewById(R.id.textToDisplay);
                try {

                    textToDisplay.setText(jsonStr);
                } catch (Exception e) {
                    Log.i("one", e.toString());
                    textToDisplay.setText(jsonStr);
                }

            } else {
                Log.e(TAG, "Couldn't get json from server.");
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(getApplicationContext(),
                                "Couldn't get json from server. Check LogCat for possible errors!",
                                Toast.LENGTH_LONG).show();
                    }
                });
            }

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);
            //Log.i("one",result.toString());

        }
    }
}
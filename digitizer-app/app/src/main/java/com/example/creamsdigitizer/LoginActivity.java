package com.example.creamsdigitizer;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.webkit.CookieManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;


public class LoginActivity extends AppCompatActivity {

    TextView txtString;

    Button b;
    EditText email;
    EditText password;
    TextView link;
    OkHttpClient client = new OkHttpClient();
    public String url= "http://creams-api.cognitiveux.net/web_app/demo/?format=openapi";

    int isLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        link = findViewById(R.id.hyperlink);
        link.setMovementMethod(LinkMovementMethod.getInstance());



        LoginButton();


    }


    private void LoginButton() {
        b = findViewById(R.id.button_login);
        email = findViewById(R.id.editText_user);
        password = findViewById(R.id.editText_password);
        txtString= (TextView)findViewById(R.id.txtString);
        b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                System.out.println("Hello");

                OkHttpHandler okHttpHandler= new OkHttpHandler();
                okHttpHandler.execute(url);

            }
        });

    }


    class OkHttpHandler extends AsyncTask <String,Void,String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected String doInBackground(String... params) {

            Request.Builder builder = new Request.Builder();

            builder.url(params[0]);
            MediaType mediaType = MediaType.parse("text/plain");
            RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
                    .addFormDataPart("email",email.getText().toString())//"creams-student@cognitiveux.de")
                    .addFormDataPart("password",password.getText().toString())//"Aa12345!")
                    .build();

            Request request = new Request.Builder()
                    .url("http://creams-api.cognitiveux.net/web_app/account-mgmt/login")
                    .method("POST", body)
                    .build();

            try {
                Response response = client.newCall(request).execute();
                CookieManager cookieManager = CookieManager.getInstance();
                String cookies = cookieManager.getCookie("access_tkn");
                if(cookies != null){
                    String[] temp=cookies.split(";");
                    for (String ar1 : temp ){
                        if(ar1.contains("access_tkn")){
                            String[] temp1=ar1.split("=");
                            //System.out.println(temp1[1]);
                        }
                    }
                }

                assert response.body() != null;
                String message = response.body().string();

                System.out.println(message);

                try {

                    JSONObject jsonObject=null;

                    jsonObject= new JSONObject(message);

                    String access = jsonObject.getString("resource_obj");

                    if(!access.equals(null))
                    {
                        System.out.println("login successful");
                        isLogin=1;

                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                    //System.out.println("login failed");
                    isLogin=0;

                }

                return message;
            }catch (Exception e){
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPreExecute() {

        }

        @Override
        protected void onPostExecute(String result)
        {

            if(isLogin==1)
            {

                Intent intent = new Intent(LoginActivity.this, TestCamera.class);
                startActivity(intent);
                Toast.makeText(LoginActivity.this, "Login success" , Toast.LENGTH_LONG).show();

            }
            else if(isLogin==0)
            {
                Toast.makeText(LoginActivity.this, "Login Failed" , Toast.LENGTH_LONG).show();
                email.setError("Check your email!");
                password.setError("Check your password");

            }

        }
    }

}
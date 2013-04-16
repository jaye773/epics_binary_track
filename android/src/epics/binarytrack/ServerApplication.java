package epics.binarytrack;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

import android.app.Application;
import android.os.Environment;
import android.util.Log;
import android.widget.Toast;
import epics.binarytrack.questions.JsonParsing;
import epics.binarytrack.questions.Question;

public class ServerApplication extends Application {

	public static Socket clientSocket = null;
	public static PrintWriter out = null;
	public static ArrayList<Question> questions=null;

	@Override
	public void onCreate() {
		super.onCreate();
		Runnable r = new Runnable() {
			@Override
			public void run() {
				ServerSocket serverSocket = null;
				while (true){
				try {
					serverSocket = new ServerSocket(8081);
					clientSocket = serverSocket.accept();
					Log.d("epics","Waiting for connection.....");
					new Thread(new Runnable(){

						@Override
						public void run() {
							try {
								out = new PrintWriter(clientSocket.getOutputStream(), true);
							} catch (IOException e) {
								Log.d("Connecting", "client did not connect");
							}
						}
						
					}).start();
				} catch (IOException e) {
					System.err.println("Could not listen on port: 10007.");
					System.exit(0);
				}
				Log.d("epics","Connection successful");
				Log.d("epics","Waiting for input.....");
				}
			}
		};
		new Thread(r).start();
		
		try {
			JsonParsing.process();
		} catch (Exception e) {
			Log.d("processing json", e.getMessage());
			e.printStackTrace();
		}
		if(JsonParsing.getList()!=null){
			Log.d("processing question", "not null");
		}
		
	}

}

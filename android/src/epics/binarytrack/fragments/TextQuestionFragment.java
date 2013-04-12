package epics.binarytrack.fragments;

import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.TextView.OnEditorActionListener;
import android.widget.Toast;
import epics.binarytrack.R;

public class TextQuestionFragment extends QuestionFragment {

	private TextView mTextView = null;
	private EditText mEditText = null;
	
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
    	View layout = inflater.inflate(R.layout.text_question, container, false);
    	mTextView = (TextView)layout.findViewById(R.id.textView1);
    	mEditText = (EditText)layout.findViewById(R.id.editText1);
    	
		mTextView.setText(mQuestion.getQuestion());
    	mEditText.setOnEditorActionListener(new OnEditorActionListener() {
			@Override
			public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
				String input = mEditText.getEditableText().toString();
				if(mQuestion.processResponse(input.trim()) ){
					Toast.makeText(TextQuestionFragment.this.getActivity(), "You are right!", Toast.LENGTH_SHORT).show();
				}else{
					Toast.makeText(TextQuestionFragment.this.getActivity(), "You are wrong!", Toast.LENGTH_SHORT).show();
				}
				mEditText.setText("");
//				InputMethodManager imm = (InputMethodManager)TextQuestionFragment.this.getActivity().getSystemService(Context.INPUT_METHOD_SERVICE);
//				imm.hideSoftInputFromWindow(mEditText.getWindowToken(), 0);
				mCallback.onQuestionAnswered();
				return true;
			}
		});
        return layout;
    }
}

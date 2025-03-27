package client;
 
import java.io.IOException;

import org.restlet.data.Form;
import org.restlet.representation.Representation;
import org.restlet.resource.ClientResource;
import org.restlet.resource.ResourceException;
 
public class ClientCall {
 
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		// Create the client resource  
		ClientResource resource = new ClientResource("http://localhost:8186/customers");  
 
		Form form = new Form();  
		form.add("cid", "12");  
		form.add("cname", "John");  
		form.add("loanType", "personal"); 
		form.add("loanAmount", "5000"); 
		form.add("loanDescription", "loan to buy a tv"); 
 
		// Write the response entity on the console
		try {
 
			resource.post(form).write(System.out); // customer creates a new loan request
			
			//TODO Customer notified to submit check OR about loan cancellation (response to SOAP request)
			
			//TODO post request to submit a check for validation (use gRPC)
		
		} catch (ResourceException e) {
			
			e.printStackTrace();
		} catch (IOException e) {
			
			e.printStackTrace();
		}  
	}
 
}
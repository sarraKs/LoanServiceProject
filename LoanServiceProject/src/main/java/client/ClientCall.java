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
		// TODO Auto-generated method stub
 
		// Create the client resource  
		ClientResource resource = new ClientResource("http://localhost:8186/users");  
 
		Form form = new Form();  
		form.add("uid", "1234");  
		form.add("uname", "John");  
 
		// Write the response entity on the console
		try {
 
			resource.post(form).write(System.out);
 
		} catch (ResourceException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}  
	}
 
}
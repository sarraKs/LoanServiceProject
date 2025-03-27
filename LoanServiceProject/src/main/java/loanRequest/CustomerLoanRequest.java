package loanRequest;

import org.restlet.data.Form;
import org.restlet.data.MediaType;
import org.restlet.representation.Representation;
import org.restlet.representation.StringRepresentation;
import org.restlet.resource.Get;
import org.restlet.resource.Post;
import org.restlet.resource.ServerResource;

public class CustomerLoanRequest extends ServerResource {

	@Get  
	public String toString() {
		String cid = (String) getRequestAttributes().get("cid");
		return "Information about customer \"" + cid + "\" is: <nothing>";  
	}  
	
	 @Post
	    public Representation acceptItem(Representation entity) {  
			Representation result = null;  
	        // Parse the given representation and retrieve data
	        Form form = new Form(entity);  
	        String cid = form.getFirstValue("cid");  
	        String cname = form.getFirstValue("cname");  
	 
	        if(cid.equals("123")){ // Assume that user id 123 is existed
	        result = new StringRepresentation("Customer whose cid="+ cid +" is updated",  
	            MediaType.TEXT_PLAIN);
	        } 
	        else { // otherwise add user  
	        result = new StringRepresentation("Customer " + cname + " is added",  
	            MediaType.TEXT_PLAIN);
	        }  
	 
	        return result;  
	    } 
}

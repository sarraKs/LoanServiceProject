package loanRequest;

import org.restlet.data.Form;
import org.restlet.data.MediaType;
import org.restlet.representation.Representation;
import org.restlet.representation.StringRepresentation;
import org.restlet.resource.Get;
import org.restlet.resource.Post;
import org.restlet.resource.ServerResource;

public class CustomerLoanRequest extends ServerResource {

	public static final String MAX_LOAN_AMOUNT = "50000"; 
	
	@Get  
	public String toString() {
		String cid = (String) getRequestAttributes().get("cid");
		return "Information about customer \"" + cid + "\" is: .... ";  
	}  
	
	 @Post
	    public Representation acceptLoanRequest(Representation entity) {  
			Representation result = null;  
	        // Parse the given representation and retrieve data
	        Form form = new Form(entity);  
	        String cid = form.getFirstValue("cid");  
	        String cname = form.getFirstValue("cname");  
	        String loanType = form.getFirstValue("loanType");
	        String loanAmount = form.getFirstValue("loanAmount");
	        String loanDescription = form.getFirstValue("loanDescription");
	 
	        
	       if (Integer.parseInt(loanAmount) > Integer.parseInt(MAX_LOAN_AMOUNT) )
	        {
	    	   result = new StringRepresentation("Customer whose cid="+ cid +" created a new loan. The amount is very high, loan declined !",  
	   	            MediaType.TEXT_PLAIN);
	       }
	       else {
	    	   result = new StringRepresentation("Customer "+ cname + " whose cid="+ cid +" created a new loan (type= "+loanType+", amount="+loanAmount+", description="+loanDescription+"). Proceeding to check the risk level...",
	    	   MediaType.TEXT_PLAIN);
	       }
	        
	       /*
	        if(cid.equals("123")){ // Assume that customer id 12 exists
	        result = new StringRepresentation("Customer whose cid="+ cid +" created a new loan",  
	            MediaType.TEXT_PLAIN);
	        } 
	        else { // otherwise add user  
	        result = new StringRepresentation("Customer " + cname + " is added",  
	            MediaType.TEXT_PLAIN);
	        }  
	 */
	        return result;  
	    } 
}

import android.util.Log;
import java.util.HashSet;
import java.util.Set;

public aspect Coverage {
	private Set<String> messages = new HashSet<>();
	
	pointcut notwithin() :
		!within(sun..*) &&
		!within(java..*) &&
		!within(javax..*) &&
		!within(jakarta..*) &&
		!within(com.sun..*) &&
		!within(android..*) &&
		!within(androidx..*) &&
		!within(kotlin..*) &&
		!within(net.sf.cglib..*) &&
		!within(org.aspectj..*) &&
		!within(com.google.android..*) &&
		!within(com.android..*) &&
		!within(com.google..*) &&
		!within(com.facebook..*) &&
		!within(org.apache..*) &&
		!within(libcore..*) &&
		!within(mop..*) &&
		!within(javamop..*) &&
		!within(javamoprt..*) &&
		!within(rvmonitorrt..*) &&
		!within(com.runtimeverification..*) && 
		!within(br.unb.cic.mop..*) &&
		!within(*..Log) &&
		!within(*..Coverage);		
	
	pointcut traced() : execution(* *.*(..)) && notwithin();
	
	before() : traced() {
		// https://eclipse.dev/aspectj/doc/released/progguide/language-thisJoinPoint.html
		// https://javadoc.io/doc/org.aspectj/aspectjweaver/1.9.2/org/aspectj/lang/JoinPoint.StaticPart.html
		String sig = thisJoinPointStaticPart.getSignature().toLongString().strip();
		String methodSignature = String.format("%s:::%s:::%s", thisJoinPointStaticPart.getSignature().getDeclaringTypeName(), thisJoinPointStaticPart.getSignature().getName(), sig.substring(sig.indexOf('(')));
		// check if the message has already been logged
		if(messages.add(methodSignature)) {
			Log.v("RVSEC-COV", methodSignature);
		}
	}
	
}
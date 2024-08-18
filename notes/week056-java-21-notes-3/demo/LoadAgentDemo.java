import com.sun.tools.attach.VirtualMachine;
import java.io.File;

public class LoadAgentDemo {
    public static void main(String... args) throws Exception {

        String pidOfOtherJVM = "3378";
        VirtualMachine vm = VirtualMachine.attach(pidOfOtherJVM);

        File agentJar = new File("/com.docker.devenvironments.code/agent-demo-1.0-SNAPSHOT-jar-with-dependencies.jar");
        vm.loadAgent(agentJar.getAbsolutePath());

        // do other works

        vm.detach();
    }
}

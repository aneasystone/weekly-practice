import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class App {
    
    public static void main( String[] args ) throws IOException {
        String message = readResource("app.res");
        System.out.println(message);
    }

    public static String readResource(String fileName) throws IOException {
        StringBuilder content = new StringBuilder();
        try (
            InputStream inputStream = App.class.getClassLoader().getResourceAsStream(fileName);
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append(System.lineSeparator());
            }
        }
        return content.toString();
    }
}
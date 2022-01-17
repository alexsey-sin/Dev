/*

*/

package scom2;

import java.util.List;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

/**
 *
 * @author а
 */
public class SCOM2 extends Application {
   public static FXMLMainController controller;
   public static List<BOND> listBOND = null;
//   public static List<TypeBOND> typeBOND = null;
   public static Stage mainStage;
    
    @Override
    public void start(Stage stage) throws Exception {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("FXMLMain.fxml"));
        Parent root = loader.load();
//        Parent root = FXMLLoader.load(getClass().getResource("FXMLMain.fxml"));
        controller = (FXMLMainController)loader.getController();
        Scene scene = new Scene(root);
        
        stage.setScene(scene);
        mainStage = stage;
        mainStage.show();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        launch(args);
    }
    
}

/*
 * 

*/

package scom2;

import java.awt.MouseInfo;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.datatransfer.StringSelection;
import java.io.File;
import java.math.BigDecimal;
import java.net.URL;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.ResourceBundle;
import javafx.application.Platform;
import javafx.beans.binding.Bindings;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.collections.ListChangeListener;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ContextMenu;
import javafx.scene.control.DatePicker;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.MenuItem;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TablePosition;
import javafx.scene.control.TableRow;
import javafx.scene.control.TableView;
import javafx.scene.control.TableView.TableViewSelectionModel;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.ContextMenuEvent;
import static javafx.scene.input.KeyCode.T;
import javafx.scene.input.MouseEvent;
import javafx.stage.FileChooser;
import javafx.util.Callback;
import org.controlsfx.control.CheckComboBox;
//import static scom2.SCOM2.typeBOND;

/**
 *
 * @author а
 */
public class FXMLMainController implements Initializable {
    private ObservableList<TableBOND> tableData = FXCollections.observableArrayList();
    private ContextMenu contextMenuTableBOND;
    
    @FXML private DatePicker matDateStart, matDateStop;
    @FXML private CheckBox checkStartFaceValue, checkStopFaceValue, checkStartMatDate, checkStopMatDate, checkType;
    @FXML private TextField startFaceValue, stopFaceValue;
    @FXML private CheckComboBox<String> comboBoxType;
    @FXML private TableView tableBond;
    @FXML private TableColumn<TableBOND, String> colSecid;
    @FXML private TableColumn<TableBOND, String> colName;
    @FXML private TableColumn<TableBOND, String> colMatDate;
    @FXML private TableColumn<TableBOND, Double> colFaceValue;
    @FXML private TableColumn<TableBOND, Integer> colCouponFrequency;
    @FXML private TableColumn<TableBOND, Double> colCouponValue;
    @FXML private TableColumn<TableBOND, String> colType;
    @FXML private TableColumn<TableBOND, Double> colProfit;
    @FXML private TextArea textarea;
    @FXML private Label lblStatus;
    
    public int delayStatusMS = 1000;

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        // устанавливаем тип и значение которое должно хранится в колонке
        colSecid.setCellValueFactory(new PropertyValueFactory<>("Secid"));
        colName.setCellValueFactory(new PropertyValueFactory<>("Name"));
        colMatDate.setCellValueFactory(new PropertyValueFactory<>("MatDate"));
        colFaceValue.setCellValueFactory(new PropertyValueFactory<>("FaceValue"));
        colCouponFrequency.setCellValueFactory(new PropertyValueFactory<>("CouponFrequency"));
        colCouponValue.setCellValueFactory(new PropertyValueFactory<>("CouponValue"));
        colType.setCellValueFactory(new PropertyValueFactory<>("Type"));
        colProfit.setCellValueFactory(new PropertyValueFactory<>("Profit"));
        
        tableBond.setRowFactory(new Callback<TableView<TableBOND>, TableRow<TableBOND>>() {
                @Override public TableRow<TableBOND> call(TableView<TableBOND> tableView) {
                    final TableRow<TableBOND> row = new TableRow<>();
                    final ContextMenu rowMenu = new ContextMenu();
                    MenuItem copySecidItem = new MenuItem("Скопировать код");
                    copySecidItem.setOnAction(new EventHandler<ActionEvent>() {
                        @Override public void handle(ActionEvent event) {
                            String str = row.getItem().getSecid();
                            StringSelection ss = new StringSelection(str);
                            Toolkit.getDefaultToolkit().getSystemClipboard().setContents(ss, null);
                        }
                    });

                    MenuItem copyRowItem = new MenuItem("Скопировать строку");
                    copyRowItem.setOnAction(new EventHandler<ActionEvent>() {
                        @Override public void handle(ActionEvent event) {
                            String str = row.getItem().getSecid() + ";" + row.getItem().getName()
                                    + ";" + row.getItem().getMatDate().toString() + ";" + Double.toString(row.getItem().getFaceValue())
                                    + ";" + Integer.toString(row.getItem().getCouponFrequency()) + ";" + Double.toString(row.getItem().getCouponValue())
                                    + ";" + row.getItem().getType();
                            StringSelection ss = new StringSelection(str);
                            Toolkit.getDefaultToolkit().getSystemClipboard().setContents(ss, null);
                        }
                    });

                    MenuItem removeItem = new MenuItem("Удалить");
                    removeItem.setOnAction(new EventHandler<ActionEvent>() {
                    @Override public void handle(ActionEvent event) {
                            tableBond.getItems().remove(row.getItem());
                        }
                    });
                    rowMenu.getItems().addAll(copySecidItem, copyRowItem, removeItem);
                    row.contextMenuProperty().bind(Bindings.when(Bindings.isNotNull(row.itemProperty())).then(rowMenu).otherwise((ContextMenu)null));
                    return row;
            }
        });
    }    
//==============================================================================
    public void OnActionMenuItemLoadOfFile(ActionEvent event) {
        FileChooser fileChooser = new FileChooser();//Класс работы с диалогом выборки и сохранения
        fileChooser.setTitle("Открыть архив");//Заголовок диалога
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("XML файлы", "*.xml"));
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Все файлы", "*.*"));
        File firstDir = new File(System.getProperty("archive.xml"), "archives");
        if(!firstDir.exists()) firstDir.mkdirs();
        fileChooser.setInitialDirectory(firstDir);
        File file = fileChooser.showOpenDialog(SCOM2.mainStage);//Указываем текущую сцену CodeNote.mainStage
        if (file != null) {
            SCOM2.listBOND = BOND.loadXMLFile(file.toPath());
            OutTableBOND();
            if(SCOM2.listBOND != null){
                LoadBondFinish();
            }
        }
    }
    public void OnActionMenuItemSaveOnFile(ActionEvent event) {
        FileChooser fileChooser = new FileChooser();//Класс работы с диалогом выборки и сохранения
        fileChooser.setTitle("Сохранить архив");//Заголовок диалога
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("XML файлы", "*.xml"));
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Все файлы", "*.*"));
        fileChooser.setInitialFileName("archive.xml");
        File firstDir = new File(System.getProperty("archive.xml"), "archives");
        if(!firstDir.exists()) firstDir.mkdirs();
        fileChooser.setInitialDirectory(firstDir);
        File file = fileChooser.showSaveDialog(SCOM2.mainStage);//Указываем текущую сцену CodeNote.mainStage
        if (file != null) {
            int cnt = 0;
            if(SCOM2.listBOND != null){
                cnt = SCOM2.listBOND.size();
                BOND.saveXMLFile(SCOM2.listBOND, file.toPath());
                SetStatus("Сохранено: " + cnt, 3000);
            }else SetStatus("Нет загруженной базы", 3000);
        }
    }
    public void OnActionMenuItemLoadOnMOEX(ActionEvent event) {
        new TheadConnect("TheadConnect").start();
    }
    public void OnActionExitApp(ActionEvent event) {
        Platform.exit();
    }
//==============================================================================
    public void handlerOnActionBnt1(ActionEvent event) {
//        List<String> lStr = new ArrayList<String>(comboBoxType.getCheckModel().getCheckedItems());
//        for(String str : lStr){
//            AppendToTextArea(str);
//        }
//        iii++;
//        AppendToTextArea("" + iii);
//        if(matDateStart.getValue() != null)
//        AppendToTextArea(matDateStart.getValue().toString());
//        else AppendToTextArea("null");
    }
    
    public void handlerOnActionBnt2(ActionEvent event) {
//        for(BOND bnd : SCOM2.listBOND){
//            AppendToTextArea(bnd.getSecid() + "    " + bnd.getName() + "    " + bnd.getType());
//        }
//        AppendToTextArea("jjjfhhdghsgs");
//        textarea.insertText(0, "jjjfhhdghsgs");
//        table1.add(10);
//        System.out.println("You clicked me!");
//        System.out.println("Main thread started...");
//        new TheadConnect("TheadConnect").start();
//        System.out.println("Main thread finished...");
    }
    
    public void handlerOnActionBnt3(ActionEvent event) {
        
    }
    public void handlerOnActionBntUpdate(ActionEvent event) {
        OutTableBOND();
    }
    private void OutTableBOND(){
        LocalDate dtStart = null;
        LocalDate dtStop = null;
        Boolean isStartDateOK, isStopDateOK, isStartFaceValueOK, isStopFaceValueOK, isTypeOK;
        double dbStartFaceValue = 0.0, dbStopFaceValue = 0.0;
        
        try{dbStartFaceValue = Double.parseDouble(startFaceValue.getText());} catch (Exception e){}
        try{dbStopFaceValue = Double.parseDouble(stopFaceValue.getText());} catch (Exception e){}
        try{dtStart = matDateStart.getValue();} catch (Exception e){}
        try{dtStop = matDateStop.getValue();} catch (Exception e){}

        if(SCOM2.listBOND == null) return;
        tableData.clear();
        
        for(BOND bnd : SCOM2.listBOND){
            if(checkStartFaceValue.isSelected() && bnd.getFaceValue() < dbStartFaceValue) isStartFaceValueOK = false; else isStartFaceValueOK = true;
            if(checkStopFaceValue.isSelected() && bnd.getFaceValue() > dbStopFaceValue) isStopFaceValueOK = false; else isStopFaceValueOK = true;
            if(checkStartMatDate.isSelected() && bnd.getMatDate().compareTo(dtStart) < 0) isStartDateOK = false; else isStartDateOK = true;
            if(checkStopMatDate.isSelected() && bnd.getMatDate().compareTo(dtStop) > 0) isStopDateOK = false; else isStopDateOK = true;
            
            isTypeOK = false;
            if(checkType.isSelected()){
                List<String> lStr = new ArrayList<String>(comboBoxType.getCheckModel().getCheckedItems());
                for(String str : lStr){
                    if(bnd.getType().equals(str)) isTypeOK = true;
                }

            }else isTypeOK = true;
                    
            if(isStartDateOK && isStopDateOK && isStartFaceValueOK && isStopFaceValueOK && isTypeOK){
                double profit = (bnd.getCouponFrequency() * bnd.getCouponValue() * 100) / bnd.getFaceValue();

                BigDecimal bdec = new BigDecimal(profit);
                bdec = bdec.setScale(2, BigDecimal.ROUND_CEILING);
                profit = bdec.doubleValue();
                
                tableData.add(new TableBOND(bnd.getSecid(),bnd.getName(),
                        bnd.getMatDate().toString(),bnd.getFaceValue(),
                        bnd.getCouponFrequency(),bnd.getCouponValue(),
                        bnd.getType(),profit));
            }
        }
        
        Comparator<TableBOND> bondComparator = Comparator.comparing(TableBOND::getProfit);
        tableData.sort(bondComparator);

        SetStatus("Всего:  " + tableData.size() + "  из: " + SCOM2.listBOND.size(), 0);
        tableBond.setItems(tableData);
    }
    public void LoadBondFinish(){
        if(SCOM2.listBOND == null || SCOM2.listBOND.isEmpty()){
            SetStatus("Нет загруженных данных.", 0);
            return;
        }
        //Заполняем коллекцию типов облигаций
        ObservableList<String> olType = FXCollections.observableArrayList();
        
        for(BOND bnd : SCOM2.listBOND){
            boolean isYes = false;
            for(String str : olType){
                if(bnd.getType().equals(str)) isYes = true;
            }
            if(isYes == false) olType.add(bnd.getType());
        }
        comboBoxType.getItems().addAll(olType);
        comboBoxType.getCheckModel().checkAll();
        
        //выводим
        OutTableBOND();
    }
//==============================================================================
    public void OnCheckStartFaceValue(ActionEvent event) {
        if(checkStartFaceValue.isSelected()) startFaceValue.setDisable(false); else startFaceValue.setDisable(true);
    }
    public void OnCheckStopFaceValue(ActionEvent event) {
        if(checkStopFaceValue.isSelected()) stopFaceValue.setDisable(false); else stopFaceValue.setDisable(true);
    }
    public void OnCheckStartMatDate(ActionEvent event) {
        if(checkStartMatDate.isSelected()) {
            if(matDateStart.getValue() == null) matDateStart.setValue(LocalDate.now());
            matDateStart.setDisable(false);
        }else{
            matDateStart.setDisable(true);
        }
    }
    public void OnCheckStopMatDate(ActionEvent event) {
        if(checkStopMatDate.isSelected()) {
            if(matDateStop.getValue() == null) matDateStop.setValue(LocalDate.now().plusYears(1));
            matDateStop.setDisable(false);
        }else{
            matDateStop.setDisable(true);
        }
    }
    public void OnCheckType(ActionEvent event) {
        if(checkType.isSelected()) comboBoxType.setDisable(false); else comboBoxType.setDisable(true);
    }
//        else AppendToTextArea("null");

//            
//        

    public void AppendToTextArea(String str){
        textarea.insertText(0, str + '\n');
    }
    public void SetStatus(String str, int delay){
//        lblStatus.setTextFill((Color)clr);   //Color.RED
        lblStatus.setText("" + str);
        if(delay > 0){
            delayStatusMS = delay;
            new TheadClearStatus(()->lblStatus.setText(""));
        }
    }
    public class TheadClearStatus extends Thread {
        final Runnable onTask;
        public TheadClearStatus(Runnable onTask) {
            this.onTask = onTask;
            start();
        }
        @Override
        public void run() {
            try {
                sleep(delayStatusMS);
            } catch (Exception e) {}
            Platform.runLater(onTask);
        }
    }
}



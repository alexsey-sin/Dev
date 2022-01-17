package scom2;

import java.io.File;
import java.nio.file.Path;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Attr;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class BOND {
    private String Secid;        //Код ценной бумаги
    private String Name;         //Полное наименование
    private LocalDate MatDate;        //Дата погашения (проверка по наличию поля)
    private double FaceValue;    //Номинальная стоимость
    private int CouponFrequency; //Периодичность выплаты купона в год
    private double CouponValue;  //Сумма купона, в валюте номинала
    private String Type;         //Тип бумаги (corporate_bond)
    private final int cntFields = 7;  //количество полей
    //проверка по валюте номинала: FACEUNIT value="SUR" и наличию всех полей
    
    public void setSecid(String str){
        this.Secid = str;
    }
    public String getSecid(){
        return Secid;
    }
    
    public void setName(String str){
        this.Name = str;
    }
    public String getName(){
        return Name;
    }
    
    public void setMatDate(LocalDate dt){
        this.MatDate = dt;
    }
    public LocalDate getMatDate(){
        return MatDate;
    }
    
    public void setFaceValue(double db){
        this.FaceValue = db;
    }
    public double getFaceValue(){
        return FaceValue;
    }
    
    public void setCouponFrequency(int i){
        this.CouponFrequency = i;
    }
    public int getCouponFrequency(){
        return CouponFrequency;
    }
    
    public void setCouponValue(double db){
        this.CouponValue = db;
    }
    public double getCouponValue(){
        return CouponValue;
    }
    
    public void setType(String str){
        this.Type = str;
    }
    public String getType(){
        return Type;
    }

    public int getCountFields(){
        return cntFields;
    }
    
    public static void saveXMLFile(List<BOND> listBND, Path file){
        //https://ru.it-brain.online/tutorial/java_xml/java_xml_quick_guide/
        
        try {
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.newDocument();
            
            // root element
            Element rows = doc.createElement("rows");
            doc.appendChild(rows);
            Attr attr;
            
//            DateFormat df = new SimpleDateFormat("y-MM-d");
            
            for (BOND bond : listBND) {
                Element row = doc.createElement("row");
                rows.appendChild(row);
                
                attr = doc.createAttribute("SECID");
                attr.setValue(bond.Secid);
                row.setAttributeNode(attr);
                
                attr = doc.createAttribute("NAME");
                attr.setValue(bond.Name);
                row.setAttributeNode(attr);
                
                attr = doc.createAttribute("MATDATE");
//                attr.setValue(df.format(bond.matdate));
                attr.setValue(bond.MatDate.toString());
                row.setAttributeNode(attr);
                
                attr = doc.createAttribute("FACEVALUE");
                attr.setValue(Double.toString(bond.FaceValue));
                row.setAttributeNode(attr);
                
                attr = doc.createAttribute("COUPONFREQUENCY");
                attr.setValue(Integer.toString(bond.CouponFrequency));
                row.setAttributeNode(attr);
                
                attr = doc.createAttribute("COUPONVALUE");
                attr.setValue(Double.toString(bond.CouponValue));
                row.setAttributeNode(attr);
                
                attr = doc.createAttribute("TYPE");
                attr.setValue(bond.Type);
                row.setAttributeNode(attr);
            }
            // write the content into xml file
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.STANDALONE, "yes");
            transformer.setOutputProperty(OutputKeys.METHOD, "xml");
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult(new File(file.toString()));
            transformer.transform(source, result);
            
        } catch (Exception ex) {
            Logger.getLogger(TheadConnect.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        
    }
    public static List<BOND> loadXMLFile(Path file){
        List<BOND> listBND = new ArrayList<>();
        
        try {
            File inputFile = new File(file.toUri());
            if(!inputFile.exists()) return listBND;
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();
            
            NodeList nListRoot = doc.getElementsByTagName("rows");
            NodeList nListRows = nListRoot.item(0).getChildNodes();
            
            int i, cnt = nListRows.getLength();
            for(i = 0; i < cnt; i++){
                Node nNode = nListRows.item(i);
                if(nNode.getNodeType() == Node.ELEMENT_NODE){
                    NamedNodeMap attr = nNode.getAttributes();
                    
                    BOND bnd = new BOND();
                    bnd.Secid = attr.getNamedItem("SECID").getNodeValue();
                    bnd.Name = attr.getNamedItem("NAME").getNodeValue();
//                    bnd.matdate = new SimpleDateFormat("y-MM-d").parse(attr.getNamedItem("MATDATE").getNodeValue());
                    bnd.MatDate = LocalDate.parse(attr.getNamedItem("MATDATE").getNodeValue());
                    bnd.FaceValue = Double.parseDouble(attr.getNamedItem("FACEVALUE").getNodeValue());
                    bnd.CouponFrequency = Integer.parseInt(attr.getNamedItem("COUPONFREQUENCY").getNodeValue());
                    bnd.CouponValue = Double.parseDouble(attr.getNamedItem("COUPONVALUE").getNodeValue());
                    bnd.Type = attr.getNamedItem("TYPE").getNodeValue();
                    
                    listBND.add(bnd);
                }
            }
         
//            SCOM2.controller.AppendToTextArea("nListRoot = " + nListRows.getLength());
            
        } catch (Exception ex) {
            Logger.getLogger(TheadConnect.class.getName()).log(Level.SEVERE, null, ex);
        }
         
        return listBND;
    }
}
//String s = "27 января 2020";
//        DateTimeFormatter df = DateTimeFormatter.ofPattern("dd MMMM yyyy").withLocale(Locale.forLanguageTag("ru-RU"));
//        LocalDate.parse(s, df);

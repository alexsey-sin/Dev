package scom2;

import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;
import java.text.ParseException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.application.Platform;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;


public class TheadConnect extends Thread {
    TheadConnect(String name){
        super(name);
    }

    @Override
    public void run(){
        List<String> listSecIdBonds;

        try {
            listSecIdBonds = GetMOEXsecidBonds();
            SCOM2.listBOND = GetMOEXBonds(listSecIdBonds);
            
            if(SCOM2.listBOND != null){
                Platform.runLater(() -> {
                    SCOM2.controller.LoadBondFinish();
                });
            }
        } catch (ParseException | ParserConfigurationException ex) {
            Logger.getLogger(TheadConnect.class.getName()).log(Level.SEVERE, null, ex);
        }
//        SCOM2.controller.AppendToTextArea("OK! Загружено: " + SCOM2.listBOND.size());
        
    }   
    List<String> GetMOEXsecidBonds(){
        String str_url = "http://iss.moex.com/iss/securities.xml?lang=ru&group_by=group&group_by_filter=stock_bonds";   //&limit=100&start=700
        List<String> outList = new ArrayList<>();
        int limit = 100, start = 0; // 7467
        
        while(true){
            try {
                URL url = new URL(str_url + "&limit=" + limit + "&start=" + start);

                URLConnection conn = url.openConnection();
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder = factory.newDocumentBuilder();
                org.w3c.dom.Document doc = (org.w3c.dom.Document)builder.parse(conn.getInputStream());

                doc.getDocumentElement().normalize();

                NodeList paperList = doc.getElementsByTagName("row");

                int i, cnt = paperList.getLength();
                if(cnt == 0) break;
                for(i = 0; i < cnt; i++){
                    Node node = paperList.item(i);
                    NamedNodeMap attr = node.getAttributes();
                    String str_secid = attr.getNamedItem("secid").getNodeValue();
                    outList.add(str_secid);
                }
             } catch (SAXException | IOException | ParserConfigurationException ex) {
                Logger.getLogger(TheadConnect.class.getName()).log(Level.SEVERE, null, ex);
            }
            start += limit;
        }
        return outList;
    }
    List<BOND> GetMOEXBonds(List<String> listSecidBOND) throws ParseException, ParserConfigurationException{
        String str_url = "http://iss.moex.com/iss/securities/"; //RU000A101PV6.xml RU000A100VY0
        List<BOND> outListBOND = new ArrayList<>();
        
//        try {
        for(String str : listSecidBOND){

            try {
                URL url = new URL(str_url + str + ".xml");
                URLConnection conn = url.openConnection();

                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder = factory.newDocumentBuilder();

                org.w3c.dom.Document doc = (org.w3c.dom.Document)builder.parse(conn.getInputStream());
                doc.getDocumentElement().normalize();


                NodeList nodeList1 = doc.getElementsByTagName("data");
                int i1, cnt1 = nodeList1.getLength();
                if(cnt1 == 0) break;
                for(i1 = 0; i1 < cnt1; i1++){
                    Node node1 = nodeList1.item(i1);
                    NamedNodeMap attr1 = node1.getAttributes();
                    if(attr1.getNamedItem("id").getNodeValue().equals("description") && node1.hasChildNodes()){
                        NodeList nodeList2 = node1.getChildNodes();
                        int i2, cnt2 = nodeList2.getLength();
                        if(cnt2 == 0) break;
                        for(i2 = 0; i2 < cnt2; i2++){
                            if(nodeList2.item(i2).getNodeType() == Node.ELEMENT_NODE && nodeList2.item(i2).getNodeName().equals("rows")){
                                NodeList nodeList3 = nodeList2.item(i2).getChildNodes();
                                int i3, cnt3 = nodeList3.getLength();
    //                                
                                if(cnt3 == 0) break;
                                BOND bnd = new BOND();
                                int cntFields = 0;
                                for(i3 = 0; i3 < cnt3; i3++){   //проход по строкам иногда содержащим "row"
                                    if(nodeList3.item(i3).getNodeType() == Node.ELEMENT_NODE && nodeList3.item(i3).getNodeName().equals("row")){
                                        Node node4 = nodeList3.item(i3);
                                        NamedNodeMap attr4 = node4.getAttributes(); //получили карту атрибутов строки
                                        
                                        if(attr4.getNamedItem("name").getNodeValue().equals("SECID")){
                                            bnd.setSecid(attr4.getNamedItem("value").getNodeValue());
                                            cntFields++;
                                        }
                                        if(attr4.getNamedItem("name").getNodeValue().equals("NAME")){
                                            bnd.setName(attr4.getNamedItem("value").getNodeValue());
                                            cntFields++;
                                        }
                                        if(attr4.getNamedItem("name").getNodeValue().equals("MATDATE")){
//                                            Date date = tryDateParse(attr4.getNamedItem("value").getNodeValue());
                                            bnd.setMatDate(LocalDate.parse(attr4.getNamedItem("value").getNodeValue()));
                                            cntFields++;
                                        }
                                        if(attr4.getNamedItem("name").getNodeValue().equals("FACEVALUE")){
                                            double db = Double.parseDouble(attr4.getNamedItem("value").getNodeValue());
                                            bnd.setFaceValue(db);
                                            cntFields++;
                                        }
                                        if(attr4.getNamedItem("name").getNodeValue().equals("COUPONFREQUENCY")){
                                            int i = Integer.parseInt(attr4.getNamedItem("value").getNodeValue());
                                            bnd.setCouponFrequency(i);
                                            cntFields++;
                                        }
                                        if(attr4.getNamedItem("name").getNodeValue().equals("COUPONVALUE")){
                                            double db = Double.parseDouble(attr4.getNamedItem("value").getNodeValue());
                                            bnd.setCouponValue(db);
                                            cntFields++;
                                        }
                                        if(attr4.getNamedItem("name").getNodeValue().equals("TYPE")){
                                            bnd.setType(attr4.getNamedItem("value").getNodeValue());
                                            cntFields++;
                                        }
                                    }
                                }
                                if(bnd.getCountFields() == cntFields) outListBOND.add(bnd);
//                                else System.out.println("Не все поля: " + str);
                            }
                        }
                    }
                }
            } catch (SAXException | IOException ex) {
                Logger.getLogger(TheadConnect.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        
        return outListBOND;
    }
//    Date tryDateParse(String dateString){   //парсинг по нескольким форматам
//        List<String> formatStrings = Arrays.asList("y-MM-d", "d.MM.y");
//        for (String formatString : formatStrings){
//            try{
//                return new SimpleDateFormat(formatString).parse(dateString);
//            }catch (ParseException e) {}
//        }
//        return null;
//    }
}
//String s = "27 января 2020";
//        DateTimeFormatter df = DateTimeFormatter.ofPattern("dd MMMM yyyy").withLocale(Locale.forLanguageTag("ru-RU"));
//        LocalDate.parse(s, df);

 //                SCOM2.controller.AppendToTextArea("row/@name = " + cnt);


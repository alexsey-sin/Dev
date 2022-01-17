package scom2;

public class TableBOND {
    private String Secid;        //Код ценной бумаги
    private String Name;         //Полное наименование
    private String MatDate;        //Дата погашения (проверка по наличию поля)
    private double FaceValue;    //Номинальная стоимость
    private int CouponFrequency; //Периодичность выплаты купона в год
    private double CouponValue;  //Сумма купона, в валюте номинала
    private String Type;         //Тип бумаги (corporate_bond)
    private double Profit;       //Доходность в %
    
    public TableBOND(String secid, String name, String matdate, double facevalue, int couponfrequency, double couponvalue, String type, double profit){
        this.Secid = secid;
        this.Name = name;
        this.MatDate = matdate;
        this.FaceValue = facevalue;
        this.CouponFrequency = couponfrequency;
        this.CouponValue = couponvalue;
        this.Type = type;
        this.Profit = profit;
    }
    
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
    
    public void setMatDate(String str){
        this.MatDate = str;
    }
    public String getMatDate(){
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

    public void setProfit(double db){
        this.Profit = db;
    }
    public double getProfit(){
        return Profit;
    }

}

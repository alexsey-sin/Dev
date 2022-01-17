package scom2;

public class TypeBOND {
    private Boolean IsCheck;
    private String Type;
    
    public TypeBOND(Boolean bln, String str){
        this.IsCheck = bln;
        this.Type = str;
    }
    public void setIsCheck(Boolean bln){
        this.IsCheck = bln;
    }
    public Boolean getIsCheck(){
        return IsCheck;
    }

    public void setType(String str){
        this.Type = str;
    }
    public String getType(){
        return Type;
    }
}

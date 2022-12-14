執行頁面:http://xyp-workproject.herokuapp.com/index/  

預計未來新增內容:  
*權限認證與管理權限認證與管理(不可以網址直連、未有權限不可操作等)      
*評論區功能  
*站內搜尋功能  

如果排版符號顯示不出請開啟http傳送  
 
****  
目前功能大致上分別有login、logout、register、信箱驗證與修改、各視圖URL互連、使用者資料(使用者後臺)
# 註冊、登入與登出
登出由於只是退出帳號權限故沒有設計專屬的html。註冊部分是以修改使django內建的```UserCreationForm```，保留警告訊息，修改部分欄位，使輸入有不合邏輯的狀況發生時顯示錯誤訊息，若無問題則```save()```。  

登入部分為呼叫```AuthenticationForm```函數對使用者於login視圖所輸入的帳號密碼做驗證，若有輸入錯誤則顯示錯誤提示，後續以```authenticate```確認使用者輸入資料是否存在資料庫中，如果存在就呼叫login函數登入。  
  
  
![login](https://user-images.githubusercontent.com/87916115/206184981-6945bdba-daeb-4bec-8d6a-0a0f9f9c2181.png)
  
  
#使用者密碼找回
此功能中使用者在未登入時可於登入介面連至遺失密碼，密碼找回頁面  
由於是未登入狀態，使用者需用註冊時之信箱，並於信箱驗證信內之URL進行密碼更改，更改後即可再次登入。  
在此功能中主要工作量為研究並修改Django內之各Form函數，使其可以更客製化，讓錯誤判斷等附加功能可以輕易使用，不用從頭設計撰寫。

![resetpassword](https://user-images.githubusercontent.com/87916115/206184036-1905d4f6-c5bc-478b-8a1a-f31a12faf8a9.png)
![lost_password](https://user-images.githubusercontent.com/87916115/206184026-46c143ee-9401-4d37-b3be-f40edb75dad7.png)


  
  
# 部落格首頁

首頁部分，前端html部分是利用網路模板(https://github.com/jukanntenn/django-blog-tutorial-templates) 以載入靜態文件(static)修改而成，主要實際操作以後端部分為重。  

首頁重點在有大量數據庫資料需要整理後傳至前端做輸出，且有許多與其他視圖做連接的項目，故在理解及整理數據庫資料上(```filter```、```annotate```等)花費較多時間，並在整理過程中也發現許多問題(有興趣請看頁面底部問題整理)，整理好後以```queryset```或```list```的格式將資料庫傳遞至html做整理後印出。  
  
    
![index](https://user-images.githubusercontent.com/87916115/205069671-49fc529b-616b-4f8d-97b9-aecec6c9a7e5.png)
  
首頁功能，左半邊呈現所有文章，並提供一部份內容預覽，排序以新上舊下方式排序;右側最新文章以「發布時間」高的在上;熱門文章以「閱讀次數」高的在上，分類功能則代表這篇文章分類(案例中以單個英文大寫字母為例)，若需新增分類目前是以只有超級使用者(管理員)可以新增，並以單對多的方式僅能選一個類別，分類後方括號則是該類別文章總數。

  
  
下圖頁面為當使用者點入某文章後所進入文章閱讀頁面，此頁面將原被壓縮內文完整呈現，並繼承首頁的右半邊功能。  
![readpost](https://user-images.githubusercontent.com/87916115/205071008-df0e5c01-b745-4520-938b-b02d01de36bd.png)



# 使用者後臺介面
此處稍微將整體試圖做變化(呈現內容改為右側)，目前提供功能大致有:新增、修改與刪除文章、查看目前自己的所有文章與顯示目前點閱率最高的文章。

## 使用者首頁
在使用者後臺首頁，目前僅設計了兩個簡單的統計功能:發布文章總數與目前點閱最高文章，幫助使用者可以更快速瞭解流量所在，後續學習過程中或許會在新增東西於此。

![myhomepage](https://user-images.githubusercontent.com/87916115/205073108-b704a164-2544-4bbc-84c5-d011ab2f7ac1.png)


## 新增、修改與刪除文章
新增、修改與刪除三功能是以django基本視圖:```CreateView```、```UpdateView```、```DeleteView```三個視圖函數實現，並在做修改或發布後會自動將修改時間、發布時間、發布作者(預設登入使用者名稱)自動一併回傳至數據庫，在下圖(上)中可發現在創建頁面是沒有這些輸入選項的。

下圖(上)為使用者新增/修改文章頁面(修改與新增設為一樣介面，但URL與後續功能有差);下圖(下)為刪除頁面，在使用者刪除前會有一個確認介面。

![post_create](https://user-images.githubusercontent.com/87916115/205073112-c2647eec-6e4f-45f2-9658-eb8fb66730aa.png)
![delete](https://user-images.githubusercontent.com/87916115/205073221-cfdfb529-5b49-4a96-bf15-2d8c257afd4c.png)

## 目前已發布文章一覽
在此功能中，使用者可以查閱所有已發布文章，並一樣是以新上舊下的方式排列，上述之修改(Edit)與刪除(Delete)功能也在此做URL連結讓使用者可快速在自己想要編輯的文章上做設定。

![allpost](https://user-images.githubusercontent.com/87916115/205073098-492d19f9-6b74-4315-90d0-f479793cc7f7.png)


##修改使用者資料
本部落格目前僅有密碼與信箱可供修改，在此後台處修改信箱，需做信箱驗證，而修改密碼則不用信箱驗證，與上述於未登入前之功能有些微差異。 

![pdm](https://user-images.githubusercontent.com/87916115/206184031-f35dfe53-edf5-424a-baac-abed6746e355.png)




****  
遇到問題與解決方式紀錄:  
Q.base.html版型雖有作用在每個呼叫的版面上，但數值不共用，造成許多同樣的程式出現在各個子模板的類與函數中  
A:用```global```解決。  

Q.html中一個```for```調用```A queryset```時若要在裡面再跑另一組```B queryset```的資料會造成排版問題(如要讓A與B兩組資料平行兩行但因為是兩個```for```重疊會造成一個成行一個成列)  
A:目前是將B的資料直接在A資料庫新增項目解決。  

Q:html中```queryset```的data無法以```data.i```結合```for i```迴圈的方式跑值，僅能以```data```、```data.name```、```data.0```or```data.1```or```data.2```......直接給數字的方式  
A:目前猜測是type問題?  

Q:將數據庫新增```AUTH_USER_MODEL```後admin後臺無法操作  
A:因db中資料```django_admin_log```還綁在原路徑檔案，所以需要刪除表後重新```migrate```，但在刪除後執行```migrate```與```makemigrations```時一直顯示無新增檔案無法```migrate```，最後發現似乎是要把平常用的```python manage.py migrate```改成```python manage.py migrate <migrate資料夾所在目錄>```即成功。  

Q:程式執行後視圖排版符號顯示不出來  
A:因為排版符號資源似乎是用網路載入，而該資源目前設定為HTTP傳輸，故若瀏覽器沒開啟允許HTTP傳輸會顯示不出(方法可參閱此:https://experienceleague.adobe.com/docs/target/using/experiences/vec/troubleshoot-composer/mixed-content.html?lang=zh-Hant )，目前尚不知如何改成HTTPS。

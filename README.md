# flet_idea_board
このアプリはFletを使った簡単なIdea Boardです。 簡単に使い方を説明します。 
## 使い方
### 1. ボードを追加する
左のサイドバーの「New Board」をクリックしてボード追加ページに移動します。    
add new boardをクリックすると、ボード名を入力するダイアログが表示されます。

![Image01](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc01.png)

ボード名を入力して「Create」をクリックするとボードが追加されます。  

![Image02](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc02.png)  

追加されたボードはサイドバーと一覧画面に表示されます。  
作成されたボードをクリックすると、ボードの編集画面に移動します。
  
![Image03](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc03.png)
### 2. ボードにオブジェクトを追加する
ボードの編集画面に移動すると、ボードにオブジェクトを追加したり、お描きすることができます。  
画面上部のコントロールバーから追加したいオブジェクトを選択し、ボード上の任意の位置をクリックするとオブジェクトが追加されます。  
今回は四角形のオブジェクトを追加してみます。  

![Image04](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc04.png)

![Image05](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc05.png)

追加されたオブジェクトをクリックすることでオブジェクト内にテキストを入力することができます。  

![Image06](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc06.png)

コントロールバーからペンのアイコンを選択すると、ボード上にお描きすることができます。  

![Image07](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc07.png)

### 3. オブジェクトを編集する
追加したオブジェクトは移動したり、リサイズしたりすることができます。 

四角、円形のオブジェクトについては、以下の操作が可能です。  
1. 左クリックでオブジェクトを選択し、ドラッグすることで移動できます。
2. 右クリックでオブジェクトを選択し、ドラッグすることでリサイズできます。

![Image08](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc08.png)

矢印のオブジェクトについては、以下の操作が可能です。矢印オブジェクトは少し操作が特殊で四角、円形のオブジェクトとは異なります。   
1. 左クリックでオブジェクトを選択し、ドラッグすることで移動できます。(ダブルクリックなし)  
2. ダブルクリックしてから左クリックでオブジェクトを選択し、ドラッグすることでリサイズできます。  

![Image09](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc09.png)

3. 右クリックでオブジェクトを選択し、ドラッグすることで矢印の方向を変更できます。 

![Image10](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc10.png)

### 4. オブジェクトを削除する
画面上部のコントロールバーからゴミ箱のアイコンを選択し、ボード上にあるオブジェクトをクリックするとオブジェクトを削除できます。    
また、ボード上にお描きした線も消しゴムのようにドラッグして削除することができます。  

![Image11](https://raw.githubusercontent.com/takeru-a/flet_idea_board/refs/heads/main/assets/doc11.png)

### 参考
レイアウト部分については、MITライセンスで提供されているAppveyor Systems Inc.のFletサンプルアプリケーションから派生したものになります。 
ロジック部分は独自に開発しました。  
[Flet sample applications flet-trello-clone](https://github.com/flet-dev/examples/tree/main/python/apps/trolli)

## License Information
This project is licensed under the MIT License.  

- The layout components are derived from Flet sample applications by Appveyor Systems Inc., licensed under the MIT License.
- The logic components are independently developed by takeru-a.  
See the [LICENSE](./LICENSE) file for full license details.
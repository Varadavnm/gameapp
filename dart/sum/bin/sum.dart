import 'package:sum/sum.dart' as sum;
import 'dart:io';

void main() {
  print('Hello world:');
  // var input1= stdin.readLineSync();
  // var input2= stdin.readLineSync();
  // if (input1==null){
  //   input1='0';
  // }
  // if (input2==null){
  //   input2='0';
  // }
  // var num1 = int.parse(input1);
  // var num2 = int.parse(input2);
//  var sum=num1+num2;
 print("Enter a  name");
 var name = stdin.readLineSync();
 if(name!=null){
 print(name.length);
 }
 
 var num4 = stdin.readLineSync();
 print(int.parse(num4!));
 for(int i=0;i<10;i++){
  print(i);


 }
List<String> name_list = ["Soorya", "Ammu"];
// name_list.add("Mitra");
// name_list.add("Siyona");
print(name_list);
print(name_list.length);
if(name_list.contains("Arya")){
print("Yes");
}
else{
  print("No");
}
print(name_list.join('*'));
name_list.removeAt(0);
print(name_list);
List<List<int>> numlist = [[1,23,45],[45,54,69],[67,65,68]];
print(numlist[1][2]);

// print(sum);
  

}

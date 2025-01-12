{$mode objfpc}{$H+}{$J-}

program Part1;

uses
  ArrayUtils, JabbaTypes, JabbaUtils, sysutils;


procedure Main();
var
  fname, line: String;
  lines, parts: TStringArray;
  col1, col2: TIntArray;
  idx: Integer = 0;
  total: Integer = 0;
begin
  // fname := 'example.txt';
  fname := 'input.txt';
  lines := Readlines(fname);
  col1 := [];
  col2 := [];
  for line in lines do
    begin
      parts := PySplit(line);
      SetLength(col1, Length(col1) + 1);
      SetLength(col2, Length(col2) + 1);
      col1[idx] := StrToInt(parts[0]);
      col2[idx] := StrToInt(parts[1]);
      idx += 1;
    end;
  SimpleSort(col1);
  SimpleSort(col2);
  for idx := Low(col1) to High(col1) do
    total += Abs(col1[idx] - col2[idx]);
  WriteLn(total);
end;

//---------------------------------------------------------------------------

begin
  WriteLn('---');
  Main();
end.

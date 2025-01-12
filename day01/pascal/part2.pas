{$mode objfpc}{$H+}{$J-}

program Part2;

uses
  ArrayUtils, JabbaTypes, JabbaUtils, sysutils;


function CountElements(const arr: array of Integer; const value: Integer): Integer;
var
  i: Integer;
begin
  Result := 0;
  for i := Low(arr) to High(arr) do
    if arr[i] = value then
      Result += 1;
end;


procedure Main();
var
  fname, line: String;
  lines, parts: TStringArray;
  col1, col2: TIntArray;
  idx: Integer = 0;
  total: Integer = 0;
  value: Integer;
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
  for idx := Low(col1) to High(col1) do
    begin
      value := col1[idx];
      total += value * CountElements(col2, value);
    end;
  WriteLn(total);
end;

//---------------------------------------------------------------------------

begin
  WriteLn('---');
  Main();
end.

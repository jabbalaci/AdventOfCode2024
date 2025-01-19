{$mode objfpc}{$H+}{$J-}

program Part2;

uses
  ArrayUtils,
  JabbaTypes,
  JabbaUtils,
  sysutils;

function is_valid(const arr: TIntArray): Boolean;
var
  i, diff: Integer;
begin
  for i := 1 to High(arr) do
    begin
      diff := Abs(arr[i-1] - arr[i]);
      if (diff < 1) or (diff > 3)  then
        Exit(False);
    end;
  Result := True;
end;

function is_safe(const arr: TIntArray): Boolean;
var
  i, diff: Integer;
  numbers: TIntArray;
begin
  for i := 0 to High(arr) do
    begin
      SetLength(numbers, length(arr));
      Move(arr[0], numbers[0], Length(arr) * SizeOf(Integer));
      Delete(numbers, i, 1);
      if IsSorted(numbers) or IsSorted(numbers, True) then
        if is_valid(numbers) then
          Exit(True);
    end;
  Result := False;
end;

procedure Main();
var
  fname, line, part: String;
  lines, parts: TStringArray;
  numbers: TIntArray;
  total: Integer = 0;
begin
  // fname := 'example.txt';
  fname := 'input.txt';

  lines := Readlines(fname);
  for line in lines do
    begin
      parts := PySplit(line);
      numbers := [];
      for part in parts do
        begin
          SetLength(numbers, Length(numbers) + 1);
          numbers[High(numbers)] := StrToInt(part);
        end;
      if is_safe(numbers) then
        total += 1;
    end;
  WriteLn(total);
end;

//---------------------------------------------------------------------------

begin
  WriteLn('---');
  Main();
end.

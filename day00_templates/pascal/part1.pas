{$mode objfpc}{$H+}{$J-}

program Part1;

uses
  ArrayUtils,
  JabbaTypes,
  JabbaUtils,
  sysutils;

procedure Main();
var
  fname, line: String;
  lines: TStringArray;
begin
  fname := 'example.txt';
  // fname := 'input.txt';

  lines := Readlines(fname);
  for line in lines do
    WriteLn(line);
end;

//---------------------------------------------------------------------------

begin
  WriteLn('---');
  Main();
end.

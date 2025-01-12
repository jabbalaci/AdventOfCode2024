{$mode objfpc}{$H+}{$J-}

unit JabbaUtils;

//---------------------------------------------------------------------------

interface

uses
  Character, JabbaTypes, sysutils;


function Input(const prompt: String = ''): String;
function PySlice(const s: string;
                 const startIndex: Integer;
                 const endIndex: Integer = MaxInt): string; overload;
function PySplit(const s: String): TStringArray;
function ToDigit(const c: Char): Integer; overload;
function ToDigit(const s: String): Integer; overload;
function Read(const FName: String; const trim: Boolean = True): String;
function Readlines(const FName: String): TStringArray;
function RemovePrefix(const s, prefix: string): string;
function RemovePostfix(const s, postfix: string): string;
function Times(const s: String; const n: Integer): String;
function Center(const s: string; width: Integer; padChar: Char = ' '): string;

//---------------------------------------------------------------------------

implementation


function Input(const prompt: String = ''): String;
var
  line: String;
begin
  Write(prompt);
  ReadLn(line);
  result := line;
end;


function PySlice(const s: string;
                 const startIndex: Integer;
                 const endIndex: Integer = MaxInt): string; overload;
var
  actualStart, actualEnd, len: Integer;
begin
  len := Length(s);

  // Handle negative indices for startIndex
  if startIndex < 0 then
    actualStart := len + startIndex
  else
    actualStart := startIndex;

  // Handle negative or default endIndex
  if endIndex = MaxInt then
    actualEnd := len  // Default to the end of the string (exclusive)
  else if endIndex < 0 then
    actualEnd := len + endIndex  // Handle negative endIndex
  else
    actualEnd := endIndex;

  // Ensure bounds are within valid range
  if actualStart < 0 then
    actualStart := 0;
  if actualEnd > len then
    actualEnd := len;

  // If start < end, return the substring; otherwise, return empty string
  if actualStart < actualEnd then
    Result := Copy(s, actualStart + 1, actualEnd - actualStart)
              // Adjust for 1-based indexing
  else
    Result := '';
  // Return empty string for invalid slices
end;


function PySplit(const s: String): TStringArray;
begin
  Result := s.Trim().Split([' ', #9, #10, #13], TStringSplitOptions.ExcludeEmpty);
end;


function ToDigit(const c: Char): Integer; overload;
begin
  if not IsDigit(c) then
    raise EValueError.Create(Format('ToDigit(): expected digit, got "%s"', [c]));
  result := ord(c) - ord('0');
end;

function ToDigit(const s: String): Integer; overload;
begin
  if Length(s) <> 1 then
    raise EValueError.Create(Format('ToDigit(): expected 1 character, got "%s"', [s]));
  // else:
  result := ToDigit(s[1]);
end;


// don't use it with big files
function Read(const FName: String; const trim: Boolean = True): String;
var
  F: TextFile;
  line: String;
begin
  Result := '';
  AssignFile(F, FName);
  Reset(F);
  while not Eof(F) do
    begin
      ReadLn(F, line);
      Result += line + LineEnding;
    end;
  CloseFile(F);
  if trim then
    Result := Result.TrimRight();
end;

// don't use it with big files
function Readlines(const FName: String): TStringArray;
var
  F: TextFile;
  line: String;
  idx: Integer = 0;
begin
  Result := [];
  AssignFile(F, FName);
  Reset(F);
  while not Eof(F) do
    begin
      ReadLn(F, line);
      SetLength(Result, Length(Result) + 1);
      Result[idx] := line;
      idx += 1;
    end;
  CloseFile(F);
end;


function RemovePrefix(const s, prefix: string): string;
begin
  Result := s;
  if s.StartsWith(prefix) then
    Result := Copy(s, Length(prefix) + 1, Length(s));
end;

function RemovePostfix(const s, postfix: string): string;
begin
  Result := s;
  if s.EndsWith(postfix) then
    Result := Copy(s, 1, Length(s) - Length(postfix));
end;


function Times(const s: String; const n: Integer): String;
var
  i: Integer;
begin
  Result := '';
  for i := 1 to n do
    Result += s;
end;


function Center(const s: string; width: Integer; padChar: Char = ' '): string;
var
  padding, leftPad: Integer;
begin
  if Length(s) >= width then
    Result := s
  else
    begin
      padding := width - Length(s);
      leftPad := padding div 2;
      Result := StringOfChar(padChar, leftPad) + s +
                StringOfChar(padChar, padding - leftPad);
    end;
end;

//---------------------------------------------------------------------------

end.

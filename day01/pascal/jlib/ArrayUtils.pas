{$mode objfpc}{$H+}{$J-}

unit ArrayUtils;

//---------------------------------------------------------------------------

interface

uses
  JabbaTypes, sysutils;

generic procedure PrintArray<T>(const arr: array of T; quote: Boolean = False); overload;
procedure PrintArray(const arr: array of Char; quote: Boolean = True); overload;
procedure PrintArray(const arr: array of Integer; quote: Boolean = False); overload;
procedure PrintArray(const arr: array of String; quote: Boolean = True); overload;
//
generic procedure ReverseOrder<T>(var arr: array of T); overload;
procedure ReverseOrder(var arr: array of Integer); overload;
procedure ReverseOrder(var arr: array of String); overload;
//
generic procedure SimpleSort<T>(var arr: array of T; const desc: Boolean = False); overload;
procedure SimpleSort(var arr: array of Integer; const desc: Boolean = False); overload;
procedure SimpleSort(var arr: array of String; const desc: Boolean = False); overload;
//
function Sum(const arr: array of Integer): Int64;
function Prod(const arr: array of Integer): Int64;
//
generic function ArraysEqual<T>(const arr1, arr2: array of T): Boolean; overload;
function ArraysEqual(const arr1, arr2: array of Integer): Boolean; overload;
function ArraysEqual(const arr1, arr2: array of String): Boolean; overload;
//
function ConcatArrays(const a, b: array of Integer): TIntArray; overload;
function ConcatArrays(const a, b: array of string): TStringArray; overload;
function PySlice(const arr: TIntArray;
                 const startIndex: Integer;
                 const endIndex: Integer = MaxInt): TIntArray; overload;

//---------------------------------------------------------------------------

implementation

generic procedure PrintArray<T>(const arr: array of T; quote: Boolean = False); overload;
var
  i: Integer;
begin
  Write('[');
  for i := 0 to High(arr) do
    begin
      if quote then
        Write('''', arr[i], '''')
      else
        Write(arr[i]);

      if i < High(arr) then
        Write(', ');
    end;
  WriteLn(']');
end;

procedure PrintArray(const arr: array of Char; quote: Boolean = True); overload;
begin
  specialize PrintArray<Char>(arr, quote);
end;

procedure PrintArray(const arr: array of Integer; quote: Boolean = False); overload;
begin
  specialize PrintArray<Integer>(arr, quote);
end;

procedure PrintArray(const arr: array of String; quote: Boolean = True); overload;
begin
  specialize PrintArray<String>(arr, quote);
end;


// reverse the order of the elements in-place
generic procedure ReverseOrder<T>(var arr: array of T);
var
  i, j: Integer;
  temp: T;
begin
  i := Low(arr);
  j := High(arr);
  while i < j do
    begin
      temp := arr[i];
      arr[i] := arr[j];
      arr[j] := temp;
      inc(i);
      dec(j);
    end;
end;

procedure ReverseOrder(var arr: array of Integer); overload;
begin
  specialize ReverseOrder<Integer>(arr);
end;

procedure ReverseOrder(var arr: array of String); overload;
begin
  specialize ReverseOrder<String>(arr);
end;

// sort the array in-place
// Slow! Use it for small arrays only.
generic procedure SimpleSort<T>(var arr: array of T; const desc: Boolean = False); overload;
var
  i, j: Integer;
  temp: T;
begin
  for i := 0 to High(arr) do
    for j := i + 1 to High(arr) do
      if arr[j] < arr[i] then
        begin
          temp := arr[i];
          arr[i] := arr[j];
          arr[j] := temp;
        end;
  if desc then
    begin
      i := Low(arr);
      j := High(arr);
      while i < j do
        begin
          temp := arr[i];
          arr[i] := arr[j];
          arr[j] := temp;
          inc(i);
          dec(j);
        end;
    end;
end;

procedure SimpleSort(var arr: array of Integer; const desc: Boolean = False); overload;
begin
  specialize SimpleSort<Integer>(arr, desc);
end;

procedure SimpleSort(var arr: array of String; const desc: Boolean = False); overload;
begin
  specialize SimpleSort<String>(arr, desc);
end;


function Sum(const arr: array of Integer): Int64;
var
  i: Integer;
begin
  Result := 0;
  for i := Low(arr) to High(arr) do
    Result += arr[i];
end;

function Prod(const arr: array of Integer): Int64;
var
  i: Integer;
begin
  Result := 1;
  for i := Low(arr) to High(arr) do
    Result *= arr[i];
end;


generic function ArraysEqual<T>(const arr1, arr2: array of T): Boolean; overload;
var
  i: Integer;
begin
  if Length(arr1) <> Length(arr2) then
    Exit(False);

  for i := 0 to Length(arr1) - 1 do
    if arr1[i] <> arr2[i] then
      Exit(False);

  Result := True;
end;

function ArraysEqual(const arr1, arr2: array of Integer): Boolean; overload;
begin
  Result := specialize ArraysEqual<Integer>(arr1, arr2);
end;

function ArraysEqual(const arr1, arr2: array of String): Boolean; overload;
begin
  Result := specialize ArraysEqual<String>(arr1, arr2);
end;


function ConcatArrays(const a, b: array of Integer): TIntArray; overload;
begin
  Result := [];
  SetLength(Result, Length(a) + Length(b));
  Move(a[0], Result[0], Length(a) * SizeOf(Integer));
  Move(b[0], Result[Length(a)], Length(b) * SizeOf(Integer));
end;

function ConcatArrays(const a, b: array of string): TStringArray; overload;
var
  i: Integer;
begin
  Result := [];
  SetLength(Result, Length(a) + Length(b));
  // Copy first array
  for i := 0 to High(a) do
    Result[i] := a[i];
  // Copy second array
  for i := 0 to High(b) do
    Result[Length(a) + i] := b[i];
end;


function PySlice(const arr: TIntArray;
                 const startIndex: Integer;
                 const endIndex: Integer = MaxInt): TIntArray; overload;
var
  actualStart, actualEnd, len: Integer;
begin
  len := Length(arr);

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
    Result := Copy(arr, actualStart, actualEnd - actualStart)
  else
    Result := [];
  // Return empty array for invalid slices
end;

//---------------------------------------------------------------------------

end.

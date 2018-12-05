program Day05;
{$H+}

function ReadFile: String;
var
  F: TextFile;
begin
  Assign(F, 'day05.in');
  Reset(F);
  ReadLn(F, ReadFile);
  Close(F);
end;

function Part1(polymer: String): String;
var
  i: Integer;
  c1, c2: Char;
begin
  i := 1;
  while i < Length(polymer) - 1 do
  begin;
    c1 := polymer[i];
    c2 := polymer[i + 1];
    if (c1 <> c2) and (LowerCase(c1) = LowerCase(c2)) then
    begin
      Delete(polymer, i, 2);
      if i > 0 then
      begin
        Dec(i);
      end;
    end
    else
    begin
      Inc(i);
    end;
  end;
  Part1 := polymer;
end;

function Part2(polymer: String): Integer;
var
  candidate: String;
  c, cup: Char;
  i, j, min, len: Integer;
begin
  min := 1719;
  SetLength(candidate, Length(polymer));
  for c := 'a' to 'z' do
  begin
    cup := UpCase(c);
    j := 0;
    for i := 1 to Length(polymer) do
      if (polymer[i] <> c) and (polymer[i] <> cup) then
      begin
        Inc(j);
        candidate[j] := polymer[i];
      end;
    SetLength(candidate, j);
    len := Length(Part1(candidate));
    if (c = 'a') or (len < min) then begin
      min := len;
    end;
  end;
  Part2 := min;
end;

var
  shortened: String;
  test2: Integer;

begin
  shortened := Part1('dabAcCaCBAcCcaDA');
  if Length(shortened) <> 10 then
    WriteLn('Test 1: failed (', shortened, ')')
  else
    WriteLn('Test 1: ok.');
  test2 := Part2(shortened);
  if test2 <> 4 then
    WriteLn('Test 2: failed (', test2, ')')
  else
    WriteLn('Test 2: ok.');

  shortened := Part1(ReadFile);
  WriteLn('Part 1: ', Length(shortened));
  WriteLn('Part 2: ', Part2(shortened));
end.

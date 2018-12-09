function day08
  [s1, s2] = solve(strread("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"));
  printf("Test 1: %d\nTest 2: %d\n", s1, s2)
  [s1, s2] = solve(load("day08.in"));
  printf("Part 1: %d\nPart 2: %d\n", s1, s2)
endfunction

function [s1, s2] = solve(nums)
  [s1, s2, new_p] = parse(nums, 1);
endfunction

function [s1, s2, new_p] = parse(nums, p)
  s1 = s2 = 0;
  num_children = nums(p);
  num_meta = nums(p + 1);
  p += 2;
  subs1 = [];
  subs2 = [];
  for ch = 1:num_children
    [ss1, ss2, p] = parse(nums, p);
    subs1 = [subs1; ss1];
    subs2 = [subs2; ss2];
  endfor
  new_p = p + num_meta;
  meta = nums(p:new_p-1);
  s1 = sum(subs1) + sum(meta);
  if (num_children > 0)
    for m = 1:length(meta)
      sub_meta = meta(m);
      if (sub_meta <= length(subs2))
        s2 += subs2(sub_meta);
      endif
    endfor
  else
    s2 = sum(meta);
  endif
endfunction
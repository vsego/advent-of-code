function res = f(serial)
    for x = 1:300
        for y = 1:300
            res(x, y) = pmodulo(floor(((x + 10) * y + serial) * (x + 10) / 100), 10) - 5;
        end
    end
endfunction

function res = shiftmat(f, t)
    res = zeros(300, 300)
    for d = f:t
        for x = 1:300-d
            res(x, x + d) = 1
        end
    end
endfunction

function res = part1(serial)
    sm = shiftmat(0, 2);
    [m, res] = max((sm * f(serial) * sm')(1:298,1:298));
endfunction

function res = part2(serial)
    M = f(serial)
    for size=1:300
        sm = shiftmat(0, size - 1);
        [m, k] = max((sm * M * sm')(1:301-size,1:301-size))
        if size == 1 | m > maxel then
            maxel = m;
            res = k;
            res(3) = size;
        end
    end
endfunction

part1(18)
part1(42)

part1(4455)
part2(4455)

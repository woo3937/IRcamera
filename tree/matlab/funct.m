function funs = funct
  funs.haarMatrix = @haarMatrix;
  funs.haarPwr    = @haarPwr;
  funs.S2imshow   = @S2imshow;
  funs.haarInd    = @haarInd;
end

function h=haarMatrix(n)
    % returns a matrix as in 
    % w = h x
    %
    % assumes a column w and column x
    level = log2(n);

    % init'ing
    h = [1];
    nc = 1/sqrt(2);
    lp = [1 1];
    hp = [1 -1];

    for i=1:level
        e = eye(size(h));
        h = nc * [kron(h, lp); kron(e, hp)];
    end

    % return...
    h = h;
end

function y=haarPwr(n)
    % sees what power each index of a haar matrix is. what level is at
    % recursively going down?
    %
    % note that this function is slow, but should only be called once.
    level = log2(n);
    y = zeros(n,n)-1;
    y(find(eye(n))) = floor(log2(0:n-1));
    y(find(y==-Inf)) = 0;

    for row=1:n
        for col=1:row
            y(col, row) = y(row, row);
        end
    end

    for col=1:n
        for row=1:col
            y(col, row) = y(col, col);
        end
    end

    %return...
    y = y;
end

function S2imshow(x, t)
    figure()
    imagesc(x)
    title(t)
    axis off
    colorbar EastOutside
end

function [y]=haarInd(ind, n)
    re = zeros(n,n);
    h = haarMatrix(n);

    % we care about the i'th coeff.
    h = h(ind,:);
    i = find(h ~= 0);

    % return...
    y = i;
end

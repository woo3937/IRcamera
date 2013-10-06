function f = FoneD
    f.haarMatrix = @haarMatrix;
    f.haarInd1D  = @haarInd1D;
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

function j=haarInd1D(i, n)
    % HAARIND1D
    % i -- what wavelet term are we interested in?
    % n -- the size of the matrix
    h = haarMatrix(n);
    j = find(h(i,:) ~= 0);

    % return...
    j = j;
end

function f = funct
    f.haarMatrix            = @haarMatrix;
    f.haarPwr               = @haarPwr;
    f.S2imshow              = @S2imshow;
    f.haarInd               = @haarInd;
    f.approxWavelet         = @approxWavelet;
    f.haarInd2D             = @haarInd2D;
    f.scaleWavelet          = @scaleWavelet;
    f.reshapeWavelet        = @reshapeWavelet;
    f.sampleInDetail        = @sampleInDetail;
    f.approxScaleAndReshape = @approxScaleAndReshape;
    f.seeWhereNonZero       = @seeWhereNonZero;
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
    % HAARIND
    re = zeros(n,n);
    h = haarMatrix(n);

    % we care about the i'th coeff.
    h = h(ind,:);
    i = find(h ~= 0);

    % return...
    y = i;
end

function w=approxWavelet(x, sampleAt, interestedIn)
    % APPROXWAVELET
    % x: the signal
    % sampleAt: where to sample. 0 for don'ts, 1 for do
    % m: how far in the tree to go down. 1 is the tree root
    % returns an unscaled wavelet in 1D
    n = size(x); n = n(1);
    h = haarMatrix(n);
    H = kron(h, h);

    % delete where we don't sample...
    s = sampleAt(:);
    i = 1:n^2;

    H = H(:, i(~~s));

    % the terms further down the tree will be zero no matter what
    terms = reshape(1:n^2, n, n);
    toKeep = terms(1:2^m, 1:2^m);
    % we must ensure that we're always sampling at the edges

    %H = H(toKeep, :);
    H = H(interestedIn, :);

    % return...
    w = H * x(~~sampleAt);
end

function i=haarInd2D(ind, n);
    % HAARIND2D
    % n as the width/height of the image.
    % ind as in which index that matters
    h = haarMatrix(n);
    H = kron(h, h);
    G = H(ind, :);
    % return...
    i = find(G ~= 0);
end

function w=scaleWavelet(w, sampleAt, m)
    % SCALEWAVELET -- scale the wavelet to so extra relative energy isn't in
    % where it samples more.
    % w -- the wavelet in 1D (even though it's 2D)
    % sampleAt -- where to sample
    % m

    [n, k] = size(sampleAt);
    idx = reshape(1:n^2, n, n);
    idx = idx(1:2^m, 1:2^m);

    % now, scale wavelet
    [lenw, junk] = size(w);
    for i=1:lenw
        ind = haarInd2D(idx(i), n);
        mm = sum(sampleAt(ind));
        n2 = size(ind); n2 = n2(2);
        factor = n2 / mm;
        w(i) = factor .* w(i);
    end

    %return...
    w = w;
end

function z=reshapeWavelet(w, m, n)
    w = reshape(w, 2^m, 2^m);
    z = zeros(n,n);
    z(1:2^m, 1:2^m) = w;
end
function s=sampleInDetail(w, sampleAt, threshold, treeLevel)
    % SAMPLEAT  -- see where sample at in more detail
    % w         -- your input signal, in the haar domain
    % sampleAt  -- where you're currently sampling
    % threshold -- where should we look more closely?
    % treeLevel -- how deep in the tree to look
    [n junk] = size(w);
    pwr = haarPwr(n)+1;
    i = find((abs(w) >= threshold) & (pwr == treeLevel));
    [ind j] = size(i);
    s = sampleAt;
    for ii=1:ind
        k = haarInd2D(i(ii), n);
        [kk jj] = size(k);
        j = k(ceil(rand()*jj));
        s(j) = 1;
    end

    % return...
    s = s;
end

function w=approxScaleAndReshape(x, sampleAt, m, interestedIn)
    [n j] = size(x);
    w = approxWavelet(x, sampleAt, interestedIn);
    w = scaleWavelet(w, sampleAt, m);
    w = reshapeWavelet(w, m, n);

    % return...
    w = w;

end

function i=seeWhereNonZero(w, threshold)
    i = find(abs(w) >= threshold);

    % return...
    i = i;
end

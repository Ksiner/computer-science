/**
 * @param {function} isBadVersion()
 * @return {function}
 */
var solution = function(isBadVersion) {
  /**
   * @param {integer} n Total versions
   * @return {integer} The first bad version
   */
  return function(n) {
      let startIndex = 0;
      let endIndex = n;

      while (true) {
          let middleIndex = Math.floor(startIndex + ((endIndex - startIndex) / 2));

          
          // check if middle version is bad
          if (isBadVersion(middleIndex) === false) {
              // middle version is good
              // checking next version
              if (isBadVersion(middleIndex + 1) === true) {
                // next version is bad
                // returning the result
                return middleIndex + 1;
              }

              // next version is also 
              startIndex = middleIndex + 1;
              continue;
          }
          
          if (endIndex - startIndex < 2) {
            return -1;
          }


          // middle version is bad
          // check if previous to middle version is also bad
          if (isBadVersion(middleIndex - 1) === false) {
              // previous version is good
              // returning the result
              return middleIndex;
          }
          
          // prev version is also bad
          // setting
          endIndex = middleIndex - 1;
      }
  };
};

console.log(solution((version) => [2].includes(version))(2))
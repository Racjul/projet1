with import <nixpkgs> {};  # Import Nixpkgs

mkShell {
  buildInputs = with python3Packages; [
python311Packages.pandas
python311Packages.matplotlib
python311Packages.numpy
  ];
  
}

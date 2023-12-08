{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
	buildInputs = with pkgs; [
		python3
		python3Packages.black
		python3Packages.numpy
		python3Packages.pycairo
		pyright
		cairo
	];

	shellHook = ''
		python3 -m venv .venv
		source .venv/bin/activate
	'';
}

# Semi-broken build system
%undefine _debugsource_packages

Name:		python-llama-cpp-python
Version:	0.3.16
Release:	1
Source0:	https://files.pythonhosted.org/packages/source/l/llama_cpp_python/llama_cpp_python-%{version}.tar.gz
Summary:	Python bindings for the llama.cpp library
URL:		https://pypi.org/project/llama-cpp-python/
License:	MIT
Group:		Development/Python
BuildSystem:	python
BuildRequires:	python
BuildRequires:	cmake
BuildRequires:	pkgconfig(flexiblas)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	python%{pyver}dist(scikit-build-core)
# Required (at least) for the OpenAI API server
Requires:	python%{pyver}dist(uvicorn)
Requires:	python%{pyver}dist(fastapi)
Requires:	python%{pyver}dist(sse-starlette)
Requires:	python%{pyver}dist(starlette-context)
# To test the OpenAI API server:
# python -m llama_cpp.server --model <model_path>

%description
Python bindings for the llama.cpp library

%build -p
export CMAKE_ARGS="-DGGML_BLAS:BOOL=ON -DGGML_BLAS_VENDOR=FlexiBLAS -DGGML_VULKAN:BOOL=ON"

%files
%{py_platsitedir}/bin
%{py_platsitedir}/include
%{py_platsitedir}/lib64
%{py_platsitedir}/llama_cpp
%{py_platsitedir}/llama_cpp_python-%{version}.dist-info

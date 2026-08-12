# ctypes bindings; no C debuginfo from the dummy cmake target.
%undefine _debugsource_packages

Name:		python-llama-cpp-python
Version:	0.3.34
Release:	2
Source0:	https://files.pythonhosted.org/packages/source/l/llama_cpp_python/llama_cpp_python-%{version}.tar.gz
Patch0:		0001-system-llama.patch
Summary:	Python bindings for the llama.cpp library
URL:		https://pypi.org/project/llama-cpp-python/
License:	MIT
Group:		Development/Python
BuildSystem:	python
BuildRequires:	python
BuildRequires:	cmake
BuildRequires:	python%{pyver}dist(scikit-build-core)
# ctypes loads the distro libllama / libmtmd (and through them system ggml).
Requires:	llama-cpp%{?_isa}
Requires:	python%{pyver}dist(numpy)
Requires:	python%{pyver}dist(diskcache)
Requires:	python%{pyver}dist(jinja2)
Requires:	python%{pyver}dist(typing-extensions)
Recommends:	ggml-backend-blas%{?_isa}
Recommends:	ggml-backend-vulkan%{?_isa}
Suggests:	ggml-backend-opencl%{?_isa}
Suggests:	ggml-backend-hip%{?_isa}
# OpenAI-compatible server extra (python -m llama_cpp.server)
Recommends:	python%{pyver}dist(uvicorn)
Recommends:	python%{pyver}dist(fastapi)
Recommends:	python%{pyver}dist(sse-starlette)
Recommends:	python%{pyver}dist(starlette-context)
Recommends:	python%{pyver}dist(pydantic-settings)
# To test the OpenAI API server:
# python -m llama_cpp.server --model <model_path>

%description
Python bindings for llama.cpp. Inference uses the system llama-cpp
package (libllama, libmtmd) and the system ggml backends
(Vulkan / OpenCL / HIP plugins), not a private copy compiled into
this wheel.

0.3.34 is the current PyPI release.

%prep
%autosetup -p1 -n llama_cpp_python-%{version}

%build -p
# Do not compile vendor/llama.cpp. The dummy cmake target is in Patch0.
export CMAKE_ARGS="-DLLAMA_BUILD:BOOL=OFF"

%install -a
# ctypes looks for llama_cpp/lib/libllama.so (and libmtmd.so). Point
# those names at the sonames shipped by llama-cpp. libggml is pulled
# in via DT_NEEDED / the ggml backend dir baked into libggml.
_lib=%{buildroot}%{py_platsitedir}/llama_cpp/lib
mkdir -p "$_lib"
ln -sf %{_libdir}/libllama.so.0 "$_lib/libllama.so"
ln -sf %{_libdir}/libmtmd.so.0 "$_lib/libmtmd.so"

%files
%{py_platsitedir}/llama_cpp
%{py_platsitedir}/llama_cpp_python-%{version}.dist-info

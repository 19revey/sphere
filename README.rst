=============
SPHERE readme
=============
Sphere is a 3D discrete element method algorithm utilizing CUDA.

Sphere is licensed under the GNU General Public License, v.3.
See license.txt for more information.

See the ``doc/`` folder for general reference.

Requirements
------------
The build requirements are:
  * A Nvidia CUDA-supported version of Linux or Mac OS X (see the `CUDA toolkit release notes <http://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html>`_ for more information)
  * The `GNU Compiler Collection <http://gcc.gnu.org/>`_ (GCC)
  * The `Nvidia CUDA toolkit and SDK <https://developer.nvidia.com/cuda-downloads>`_

The runtime requirements are:
  * A `CUDA-enabled GPU <http://www.nvidia.com/object/cuda_gpus.html>`_ with compute capability 1.1 or greater.
  * A Nvidia CUDA-enabled GPU and device driver

Optional tools, required for simulation setup and data processing:
  * `Python 2.7 <http://www.python.org/getit/releases/2.7/>`_
  * `Numpy <http://numpy.scipy.org>`_
  * `Matplotlib <http://matplotlib.org>`_
  * `Imagemagick <http://www.imagemagick.org/script/index.php>`_
  * `ffmpeg <http://ffmpeg.org/>`_

Optional tools, required for building the documentation:
  * `Sphinx <http://sphinx-doc.org>`_
  * `Doxygen <http://www.stack.nl/~dimitri/doxygen/>`_
  * `Breathe <http://michaeljones.github.com/breathe/>`_

Obtaining SPHERE
----------------
The best way to keep up to date with subsequent updates, bugfixes
and development, is to use the Git version control system.

To obtain a local copy, execute:
  ``git clone https://github.com/anders-dc/sphere.git``

Build instructions
------------------
  ``cd src/ && make``

This will generate a command-line executable in the root folder.

cmake_minimum_required(VERSION 2.8.9)

project(PercutaneousApproachAnalysis)

#-----------------------------------------------------------------------------
set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/PercutaneousApproachAnalysis")
set(EXTENSION_CATEGORY "IGT")
set(EXTENSION_CONTRIBUTORS "Koichiro Murakami (Shiga University of Medical Science, Japan, SPL), Atsushi Yamada (Shiga University of Medical Science, Japan), Laurent Chauvin (SPL), Junichi Tokuda (SPL)")
set(EXTENSION_DESCRIPTION "The Percutaneous Approach Analysis is used to calculate and visualize the accessibility of liver tumor with a percutaneous approach.")
set(EXTENSION_ICONURL "http://www.slicer.org/slicerWiki/images/a/ac/PAAlogo-small.png")
set(EXTENSION_SCREENSHOTURLS "http://www.slicer.org/slicerWiki/images/4/42/Accessibility_clinical.png")

#-----------------------------------------------------------------------------
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
add_subdirectory(PercutaneousApproachAnalysis)

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})

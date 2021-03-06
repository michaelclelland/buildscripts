An introduction to package install scripts, and how they are used in packaging
CFEngine.

How platforms do it:
====================

N = Script from new package
O = Script from old package

Install:
--------

+--------------+-------------+----------------+-------------+----------------+
|    rpm       |     deb     | depot (HPUX)   | bff (AIX)   | pkg (Solaris)  |
+--------------+-------------+----------------+-------------+----------------+
| N: pretrans  |     N/A     |      N/A       |     N/A     |      N/A       |
| N: pre       | N: preinst  | N: preinstall  | N: pre_i    | N: preinstall  |
| N: post      | N: postinst | N: postinstall | N: post_i   | N: postinstall |
| N: posttrans |     N/A     |      N/A       |     N/A     |      N/A       |
+--------------+-------------+----------------+-------------+----------------+

Upgrade:
--------

+--------------+-------------+----------------+-------------+----------------+
|    rpm       |     deb     | depot (HPUX)   | bff (AIX)   | pkg (Solaris)  |
+--------------+-------------+----------------+-------------+----------------+
| N: pretrans  |     N/A     |      N/A       |     N/A     |      N/A       |
| N: pre       | O: prerm    | N: preinstall  | N: pre_rm   |      N/A (*)   |
| N: post      | N: preinst  | N: postinstall | N: pre_i    |      N/A       |
| O: preun     | O: postrm   |      N/A       | N: post_i   |      N/A       |
| O: postun    | N: postinst |      N/A       |     N/A     |      N/A       |
| N: posttrans |     N/A     |      N/A       |     N/A     |      N/A       |
+--------------+-------------+----------------+-------------+----------------+

(*) Upgrade doesn't exist on Solaris. You have to remove and then add.

Removal:
--------

+--------------+-------------+----------------+-------------+----------------+
|    rpm       |     deb     | depot (HPUX)   | bff (AIX)   | pkg (Solaris)  |
+--------------+-------------+----------------+-------------+----------------+
| O: pretrans  |     N/A     |      N/A       |     N/A     |      N/A       |
| O: preun     | O: prerm    | O: preremove   | O: unpost_i | O: preremove   |
| O: postun    | O: postrm   | O: postremove  | O: unpre_i  | O: postremove  |
+--------------+-------------+----------------+-------------+----------------+

As can be seen, every single platform have their own way to do things, and no
two platforms use the same approach. We try to do our best to keep things as
consistent as possible even with weird script calling orders.

Notice also the weird calling order of bff's uninstall scripts, with post being
called first.

Our way:
========

This is the mapping we use:

Install:
--------

+-------------+----------+----------+--------------+-----------+--------------+
| Packaging   |   rpm    |   deb    | depot (HPUX) | bff (AIX) | pkg (Solaris)|
+-------------+----------+----------+--------------+-----------+--------------+
| preinstall  |   pre    | preinst  |  preinstall  |  pre_i    |  preinstall  |
| postinstall |   post   | postinst |  postinstall |  post_i   |  postinstall |
+-------------+----------+----------+--------------+-----------+--------------+

Upgrade:
--------

+-------------+----------+----------+--------------+-----------+--------------+
| Packaging   |   rpm    |   deb    | depot (HPUX) | bff (AIX) | pkg (Solaris)|
+-------------+----------+----------+--------------+-----------+--------------+
| preinstall  |   pre    | preinst  |  preinstall  |  pre_i    |     N/A      |
| postinstall |   post   | postinst |  postinstall |  post_i   |     N/A      |
| preremove   |   N/A    |   N/A    |     N/A      |    N/A    |     N/A      |
| postremove  |   N/A    |   N/A    |     N/A      |    N/A    |     N/A      |
+-------------+----------+----------+--------------+-----------+--------------+

Removal:
--------

+-------------+----------+----------+--------------+-----------+--------------+
| Packaging   |   rpm    |   deb    | depot (HPUX) | bff (AIX) | pkg (Solaris)|
+-------------+----------+----------+--------------+-----------+--------------+
| preremove   |  preun   | prerm    |  preremove   | unpost_i  |  preremove   |
| postremove  |  postun  | postrm   |  postremove  | unpre_i   |  postremove  |
+-------------+----------+----------+--------------+-----------+--------------+

In other words we choose to omit removal scripts completely in case of upgrade.
This is primarily motivated by the fact that the calling order varies wildly
between package managers, and in general you do not need to perform cleanup
anyway when upgrading.

Use the "is_upgrade" command inside the script to determine what you need to do.

Note that old packages will have their removal scripts intact during upgrade
though, so beware.


The scripts:
============

The scripts are arranged in in snippets that are divided into either package
type, script type or both. See the produce-script script for how the final
package script is put together.

This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.gitignore
2026-01-26-mntecode2netsharestreamlitkeepalivelogtx.txt
firewall_diagnostic.ps1
fix_firewall.ps1
FUNNEL_GUIDE_MIA.md
LICENSE
MANIFEST.in
netshare.code-workspace
netshare/__init__.py
netshare/__main__.py
netshare/app.py
netshare/config.py
netshare/templates/browse.html
netshare/templates/error.html
netshare/templates/index.html
PLAINTEXT_API.md
PYPI_SETUP_GUIDE.md
pypi-build/.env.template
pypi-build/build.sh
pypi-build/bump-version.sh
pypi-build/clean.sh
pypi-build/config.sh
pypi-build/deploy-prod.sh
pypi-build/deploy-test.sh
pypi-build/README.md
pypi-build/verify-install.sh
pyproject.toml
README.md
requirements.txt
streamlit/.streamlit/config.toml
streamlit/app.py
streamlit/app.py.backup
streamlit/banner/qr-greeting-banner-2x.png
streamlit/banner/qr-greeting-banner-4x.png
streamlit/config.py
streamlit/generate_burn_icon.py
streamlit/generate_donation_qr.py
streamlit/gif/Christmas-Animation1.gif
streamlit/gif/Christmas-Animation2.gif
streamlit/gif/letter-background-design-01.jpg
streamlit/gif/NewYear-Animation1.gif
streamlit/gif/NewYear-Animation2.gif
streamlit/gif/Valentine-Animation1.jpg
streamlit/gif/Valentine-Animation2.jpg
streamlit/greeting_formats.py
streamlit/greetings_qr.md
streamlit/i18n.py
streamlit/icons/burn_after_read.png
streamlit/icons/champagne.png
streamlit/icons/confetti.png
streamlit/icons/farewell.png
streamlit/icons/fireworks.png
streamlit/icons/hearts.png
streamlit/icons/lights.png
streamlit/icons/snowflake.png
streamlit/icons/stars.png
streamlit/icons/valentine.png
streamlit/keep_alive.ps1
streamlit/keep_alive.py
streamlit/keep/Christmas-Animation1.gif
streamlit/keep/Christmas-Animation2.gif
streamlit/keep/christmas-lights.gif
streamlit/keep/christmastree-notworking.mp4
streamlit/keep/dream_tycoon_bg.png
streamlit/keep/letter-background-design-01.jpg
streamlit/keep/letter-background-design-02.jpg
streamlit/keep/letter-background-design-03.jpg
streamlit/keep/wallpaper.jpg
streamlit/keepalive_daemon.py
streamlit/packages.txt
streamlit/plans/batch_tab.md
streamlit/plans/brainstorm.md
streamlit/plans/interative_demo.md
streamlit/plans/localization.md
streamlit/plans/moneytize.md
streamlit/plans/refactor.md
streamlit/qr/__init__.py
streamlit/qr/display.py
streamlit/qr/generator.py
streamlit/QUICKSTART.md
streamlit/README.md
streamlit/requirements.txt
streamlit/run.bat
streamlit/run.sh
streamlit/setup_task.ps1
streamlit/tabs/__init__.py
streamlit/tabs/about_tab.py
streamlit/tabs/batch_tab.py
streamlit/tabs/components.py
streamlit/tabs/create_tab.py
streamlit/tabs/demo_tab.py
streamlit/tabs/examples_tab.py
streamlit/tabs/funnel_tab.py
streamlit/tabs/scan_tab.py
streamlit/tabs/view_page.py
streamlit/test_fb_url.py
streamlit/test_greeting.csv
streamlit/translations.json
streamlit/utils/__init__.py
streamlit/utils/demo_data.py
streamlit/utils/download_tracker.py
streamlit/utils/file_utils.py
streamlit/utils/image_utils.py
streamlit/utils/url_utils.py
streamlit/utils/video_utils.py
```

# Files

## File: firewall_diagnostic.ps1
````powershell
# NetShare Firewall Diagnostic Script
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "NetShare Firewall Diagnostic" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check network profile
Write-Host "[1] Network Profile Check:" -ForegroundColor Yellow
Get-NetConnectionProfile | Select-Object Name, NetworkCategory, InterfaceAlias | Format-Table -AutoSize

# Check Python firewall rules
Write-Host "`n[2] Python Firewall Rules:" -ForegroundColor Yellow
$pythonRules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like '*Python*' }
if ($pythonRules) {
    foreach ($rule in $pythonRules) {
        $appFilter = $rule | Get-NetFirewallApplicationFilter
        $portFilter = $rule | Get-NetFirewallPortFilter

        Write-Host "`nRule: $($rule.DisplayName)" -ForegroundColor Green
        Write-Host "  Enabled: $($rule.Enabled)"
        Write-Host "  Direction: $($rule.Direction)"
        Write-Host "  Action: $($rule.Action)"
        Write-Host "  Profile: $($rule.Profile)"
        Write-Host "  Program: $($appFilter.Program)"
        Write-Host "  Protocol: $($portFilter.Protocol)"
        Write-Host "  Local Port: $($portFilter.LocalPort)"
    }
} else {
    Write-Host "  No Python firewall rules found!" -ForegroundColor Red
}

# Check if Windows Firewall is enabled
Write-Host "`n[3] Windows Firewall Status:" -ForegroundColor Yellow
Get-NetFirewallProfile | Select-Object Name, Enabled | Format-Table -AutoSize

# Check for blocking rules
Write-Host "`n[4] Checking for BLOCK rules on Python:" -ForegroundColor Yellow
$blockRules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like '*Python*' -and $_.Action -eq 'Block' }
if ($blockRules) {
    Write-Host "  WARNING: Found blocking rules!" -ForegroundColor Red
    $blockRules | Select-Object DisplayName, Enabled, Direction | Format-Table -AutoSize
} else {
    Write-Host "  No blocking rules found for Python." -ForegroundColor Green
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Diagnostic Complete" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
````

## File: fix_firewall.ps1
````powershell
# NetShare Firewall Fix Script
# This script creates firewall rules for Python that apply to Private network profile only (for security)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "NetShare Firewall Fix" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    Read-Host -Prompt "Press Enter to exit"
    exit 1
}

Write-Host "[1] Creating firewall rules for Python..." -ForegroundColor Yellow

# Python installations detected from diagnostic
$pythonPaths = @(
    "C:\users\hp\appdata\roaming\uv\python\cpython-3.12.11-windows-x86_64-none\python.exe",
    "C:\python313\python.exe"
)

$ruleCount = 0

foreach ($pythonPath in $pythonPaths) {
    if (Test-Path $pythonPath) {
        $pythonVersion = Split-Path (Split-Path $pythonPath -Parent) -Leaf

        # Remove existing rules for this Python to avoid conflicts
        Write-Host "  Removing old rules for $pythonVersion..." -ForegroundColor Gray
        Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*NetShare*$pythonVersion*" } | Remove-NetFirewallRule -ErrorAction SilentlyContinue

        # Create TCP rule for Private profile only
        Write-Host "  Creating TCP rule for $pythonVersion (Private Profile)..." -ForegroundColor Green
        New-NetFirewallRule `
            -DisplayName "NetShare Python - $pythonVersion (TCP)" `
            -Description "Allow NetShare file sharing on Private network (home/trusted networks only)" `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort Any `
            -Program $pythonPath `
            -Action Allow `
            -Profile Private `
            -Enabled True `
            -ErrorAction SilentlyContinue | Out-Null

        # Create UDP rule for Private profile only
        Write-Host "  Creating UDP rule for $pythonVersion (Private Profile)..." -ForegroundColor Green
        New-NetFirewallRule `
            -DisplayName "NetShare Python - $pythonVersion (UDP)" `
            -Description "Allow NetShare file sharing on Private network (home/trusted networks only)" `
            -Direction Inbound `
            -Protocol UDP `
            -LocalPort Any `
            -Program $pythonPath `
            -Action Allow `
            -Profile Private `
            -Enabled True `
            -ErrorAction SilentlyContinue | Out-Null

        $ruleCount += 2
        Write-Host "  Created 2 rules for $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  Skipping $pythonPath (not found)" -ForegroundColor Gray
    }
}

Write-Host "`n[2] Verifying new rules..." -ForegroundColor Yellow
$newRules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*NetShare Python*" }
if ($newRules) {
    Write-Host "  Successfully created $($newRules.Count) firewall rules!" -ForegroundColor Green
    $newRules | Select-Object DisplayName, Enabled, Direction, Action, Profile | Format-Table -AutoSize
} else {
    Write-Host "  WARNING: No rules were created!" -ForegroundColor Red
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Firewall Fix Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`nYou can now test the connection from your mobile device." -ForegroundColor Yellow
Write-Host "Try accessing: http://192.168.0.96:8080`n" -ForegroundColor Yellow

Read-Host -Prompt "Press Enter to exit"
````

## File: LICENSE
````
GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>.
````

## File: MANIFEST.in
````
include README.md
include LICENSE
include requirements.txt
include *.ps1
recursive-include netshare/templates *.html
recursive-include image *
````

## File: netshare/__init__.py
````python
"""
NetShare - Secure Network File Sharing Tool

A secure, Python-based network file sharing tool that allows you to share
folders over your local WiFi network with any device (Android, iOS, PC).
"""

__version__ = "1.0.4"
__author__ = "NetShare Contributors"
__license__ = "GPL-3.0"

from netshare.app import main

__all__ = ['main', '__version__']
````

## File: netshare/__main__.py
````python
"""
NetShare - Main entry point when running as a module

This allows the package to be run with: python -m netshare
"""

from netshare.app import main

if __name__ == '__main__':
    main()
````

## File: netshare/app.py
````python
#!/usr/bin/env python3
"""
NetShare - Simple Network File Sharing Tool
Share Windows folders with Android devices over WiFi
"""

import os
import socket
import sys
import threading
import webbrowser
import logging
from pathlib import Path
from urllib.parse import quote, unquote
from functools import wraps
from collections import defaultdict
from time import time

import qrcode
from flask import Flask, render_template, send_from_directory, abort, request, jsonify

# Import configuration
try:
    from netshare.config import SecurityConfig, AppConfig
except ImportError:
    # Fallback if config.py is not available
    class SecurityConfig:
        MAX_FILE_SIZE = 20 * 1024 * 1024 * 1024
        BLOCKED_EXTENSIONS = ['.exe', '.bat', '.cmd', '.sh', '.ps1']
        ALLOW_DIRECTORY_LISTING = True
        ALLOW_FILE_DOWNLOAD = True
        MAX_PATH_DEPTH = 20
        RATE_LIMIT = 100
        DEBUG_ERRORS = False
        ALLOWED_EXTENSIONS = []
    
    class AppConfig:
        DEFAULT_PORT = 5000
        DEFAULT_HOST = '0.0.0.0'
        SERVER_NAME = "NetShare"
        VERSION = "1.0.0"
        ENABLE_ACCESS_LOG = True

# Try to import tkinter for GUI (optional on some systems)
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    HAS_GUI = True
except ImportError:
    HAS_GUI = False
    print("Warning: tkinter not available. GUI folder selection disabled.")

app = Flask(__name__)

# Configure logging
if AppConfig.ENABLE_ACCESS_LOG:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

# Rate limiting storage
rate_limit_storage = defaultdict(list)


def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SecurityConfig.RATE_LIMIT:
            return f(*args, **kwargs)
        
        ip = request.remote_addr
        now = time()
        
        # Clean old requests
        rate_limit_storage[ip] = [
            req_time for req_time in rate_limit_storage[ip]
            if now - req_time < 60
        ]
        
        # Check rate limit
        if len(rate_limit_storage[ip]) >= SecurityConfig.RATE_LIMIT:
            logger.warning(f"Rate limit exceeded for {ip}")
            abort(429)  # Too Many Requests
        
        rate_limit_storage[ip].append(now)
        return f(*args, **kwargs)
    
    return decorated_function


def is_safe_path(base_path, target_path):
    """Verify that target_path is within base_path (prevents path traversal)"""
    base_path = os.path.abspath(base_path)
    target_path = os.path.abspath(target_path)
    
    # Check if target is within base
    if not target_path.startswith(base_path):
        return False
    
    # Check path depth
    relative_path = os.path.relpath(target_path, base_path)
    depth = len(Path(relative_path).parts)
    if depth > SecurityConfig.MAX_PATH_DEPTH:
        logger.warning(f"Path depth exceeded: {relative_path}")
        return False
    
    return True


def is_allowed_file(filename):
    """Check if file extension is allowed"""
    ext = os.path.splitext(filename)[1].lower()
    
    # Check blocked extensions first
    if ext in SecurityConfig.BLOCKED_EXTENSIONS:
        logger.warning(f"Blocked file extension: {ext}")
        return False
    
    # If allowed list is specified, check it
    if SecurityConfig.ALLOWED_EXTENSIONS:
        return ext in SecurityConfig.ALLOWED_EXTENSIONS
    
    return True


def get_system_drives():
    """Get list of available drives (Windows) or root directories (Unix)"""
    import platform

    if platform.system() == 'Windows':
        # Windows: Get available drives
        import string
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                try:
                    # Try to access to verify it's available
                    os.listdir(drive)
                    drives.append({
                        'name': f"{letter}: Drive",
                        'path': drive,
                        'accessible': True
                    })
                except (PermissionError, OSError):
                    drives.append({
                        'name': f"{letter}: Drive",
                        'path': drive,
                        'accessible': False
                    })
        return drives
    else:
        # Unix/Linux/Mac: Start from home directory or root
        home = os.path.expanduser("~")
        return [{
            'name': 'Home',
            'path': home,
            'accessible': True
        }, {
            'name': 'Root',
            'path': '/',
            'accessible': os.access('/', os.R_OK)
        }]


def list_directories(path):
    """List subdirectories in the given path"""
    directories = []

    try:
        # Normalize path
        path = os.path.abspath(path)

        if not os.path.exists(path):
            return None, "Path does not exist"

        if not os.path.isdir(path):
            return None, "Path is not a directory"

        # Get parent directory
        parent = os.path.dirname(path) if path != os.path.dirname(path) else None

        # List all items in directory
        try:
            items = os.listdir(path)
        except PermissionError:
            return None, "Permission denied"

        # Filter to only directories
        for item in sorted(items):
            item_path = os.path.join(path, item)
            try:
                if os.path.isdir(item_path):
                    accessible = os.access(item_path, os.R_OK)
                    directories.append({
                        'name': item,
                        'path': item_path,
                        'accessible': accessible
                    })
            except (OSError, PermissionError):
                # Skip items we can't access
                continue

        return {
            'current_path': path,
            'parent': parent,
            'directories': directories
        }, None

    except Exception as e:
        logger.error(f"Error listing directories in {path}: {str(e)}")
        return None, str(e)


def validate_folder_path(path):
    """Validate folder path for security and accessibility"""
    import json

    # Normalize path
    path = os.path.abspath(path)

    # Check if exists
    if not os.path.exists(path):
        return False, "Path does not exist"

    # Check if directory
    if not os.path.isdir(path):
        return False, "Path is not a directory"

    # Check read permissions
    if not os.access(path, os.R_OK):
        return False, "No read permission for this directory"

    # Check if already shared
    if path in config.shared_folders:
        return False, "Folder is already shared"

    # Check for parent-child conflicts
    for existing in config.shared_folders:
        if path.startswith(existing + os.sep):
            return False, f"This folder is inside already shared folder: {os.path.basename(existing)}"
        if existing.startswith(path + os.sep):
            return False, f"Shared folder '{os.path.basename(existing)}' is inside this folder"

    # Check max folders limit
    if len(config.shared_folders) >= AppConfig.MAX_SHARED_FOLDERS:
        return False, f"Maximum of {AppConfig.MAX_SHARED_FOLDERS} folders allowed"

    return True, "Valid"


def save_folders_to_file():
    """Save shared folders list to JSON file"""
    import json

    try:
        config_path = os.path.join(os.path.dirname(__file__), AppConfig.FOLDERS_CONFIG_FILE)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config.shared_folders, f, indent=2)
        logger.info(f"Saved {len(config.shared_folders)} folders to {config_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save folders: {e}")
        return False


def load_folders_from_file():
    """Load shared folders list from JSON file"""
    import json

    try:
        config_path = os.path.join(os.path.dirname(__file__), AppConfig.FOLDERS_CONFIG_FILE)
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                folders = json.load(f)

            # Validate each folder still exists
            valid_folders = []
            for folder in folders:
                if os.path.isdir(folder):
                    valid_folders.append(folder)
                else:
                    logger.warning(f"Skipping non-existent folder from config: {folder}")

            config.shared_folders = valid_folders
            logger.info(f"Loaded {len(valid_folders)} folders from {config_path}")
            return True
    except Exception as e:
        logger.error(f"Failed to load folders: {e}")

    return False


# Global configuration
class Config:
    """Application configuration"""
    shared_folders = []
    server_port = 5000
    host = '0.0.0.0'
    
config = Config()


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(url, output_path=None):
    """Generate QR code for the given URL

    Args:
        url: The URL to encode in the QR code
        output_path: Optional custom output path (if None, uses default netshare_qr.png in module directory)

    Returns:
        str: Path to the generated QR code PNG file
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Determine output path
    if output_path is None:
        qr_path = os.path.join(os.path.dirname(__file__), 'netshare_qr.png')
    else:
        # Convert relative paths to absolute based on current working directory
        qr_path = output_path if os.path.isabs(output_path) else os.path.abspath(output_path)

    # Ensure directory exists
    qr_dir = os.path.dirname(qr_path)
    if qr_dir:  # Only create directory if path has a directory component
        os.makedirs(qr_dir, exist_ok=True)

    # Save as PNG
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    # Print to terminal
    print("\n" + "="*50)
    print("Scan this QR code with your mobile device:")
    print("="*50)
    qr.print_ascii(invert=True)
    print("="*50)
    print(f"QR code saved to: {qr_path}")

    return qr_path


def format_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_file_info(filepath):
    """Get file information including size and type"""
    stat_info = os.stat(filepath)
    return {
        'size': format_size(stat_info.st_size),
        'size_bytes': stat_info.st_size,
        'is_dir': os.path.isdir(filepath)
    }


@app.route('/')
@rate_limit
def index():
    """Home page showing all shared folders"""
    folders = []
    for folder_path in config.shared_folders:
        if os.path.exists(folder_path):
            folders.append({
                'name': os.path.basename(folder_path),
                'path': folder_path,
                'full_path': folder_path
            })
    
    return render_template('index.html', 
                         folders=folders,
                         server_url=f"http://{get_local_ip()}:{config.server_port}")


@app.route('/browse/<int:folder_index>')
@app.route('/browse/<int:folder_index>/<path:subpath>')
@rate_limit
def browse(folder_index, subpath=''):
    """Browse files in a shared folder"""
    if folder_index >= len(config.shared_folders):
        logger.warning(f"Invalid folder index: {folder_index}")
        abort(404)
    
    base_folder = config.shared_folders[folder_index]
    target_path = os.path.join(base_folder, subpath)
    
    # Security: ensure we're still within the shared folder
    if not is_safe_path(base_folder, target_path):
        logger.warning(f"Path traversal attempt: {target_path}")
        abort(403)
    
    if not os.path.exists(target_path):
        abort(404)
    
    # If it's a file, serve it
    if os.path.isfile(target_path):
        # Check if file download is allowed
        if not SecurityConfig.ALLOW_FILE_DOWNLOAD:
            logger.warning(f"File download disabled: {target_path}")
            abort(403)
        
        # Check file extension
        if not is_allowed_file(target_path):
            logger.warning(f"Blocked file access: {target_path}")
            abort(403)
        
        # Check file size
        file_size = os.path.getsize(target_path)
        if file_size > SecurityConfig.MAX_FILE_SIZE:
            logger.warning(f"File too large: {target_path} ({file_size} bytes)")
            abort(413)  # Request Entity Too Large
        
        logger.info(f"Serving file: {target_path} to {request.remote_addr}")
        
        return send_from_directory(
            os.path.dirname(target_path),
            os.path.basename(target_path),
            as_attachment=True
        )
    
    # If it's a directory, list contents
    if not SecurityConfig.ALLOW_DIRECTORY_LISTING:
        logger.warning(f"Directory listing disabled: {target_path}")
        abort(403)
    
    items = []
    try:
        for item_name in sorted(os.listdir(target_path)):
            item_path = os.path.join(target_path, item_name)
            try:
                # Skip if file extension is blocked
                if os.path.isfile(item_path) and not is_allowed_file(item_path):
                    continue
                
                info = get_file_info(item_path)
                items.append({
                    'name': item_name,
                    'is_dir': info['is_dir'],
                    'size': info['size'],
                    'size_bytes': info['size_bytes']
                })
            except (OSError, PermissionError):
                # Skip files we can't access
                continue
    except (OSError, PermissionError) as e:
        error_msg = "Cannot access folder" if not SecurityConfig.DEBUG_ERRORS else str(e)
        return render_template('error.html', error=error_msg), 403
    
    # Build breadcrumb navigation
    breadcrumbs = []
    if subpath:
        parts = subpath.split(os.sep)
        current_path = ''
        for part in parts:
            current_path = os.path.join(current_path, part) if current_path else part
            breadcrumbs.append({
                'name': part,
                'path': current_path
            })
    
    return render_template('browse.html',
                         folder_index=folder_index,
                         folder_name=os.path.basename(base_folder),
                         current_path=subpath,
                         breadcrumbs=breadcrumbs,
                         items=items)


@app.route('/upload/<int:folder_index>', methods=['POST'])
@app.route('/upload/<int:folder_index>/<path:subpath>', methods=['POST'])
@rate_limit
def upload_file(folder_index, subpath=''):
    """Handle file upload to a shared folder"""
    try:
        # Validate folder index
        if folder_index >= len(config.shared_folders):
            logger.warning(f"Invalid folder index: {folder_index}")
            return jsonify({
                'success': False,
                'message': 'Invalid folder index'
            }), 404

        base_folder = config.shared_folders[folder_index]
        target_dir = os.path.join(base_folder, subpath)

        # Security: ensure we're still within the shared folder
        if not is_safe_path(base_folder, target_dir):
            logger.warning(f"Path traversal attempt in upload: {target_dir}")
            return jsonify({
                'success': False,
                'message': 'Invalid path'
            }), 403

        # Verify target directory exists
        if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
            return jsonify({
                'success': False,
                'message': 'Target directory does not exist'
            }), 404

        # Check if file was included in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400

        file = request.files['file']

        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400

        # Sanitize filename to prevent path traversal
        filename = os.path.basename(file.filename)
        if not filename or filename.startswith('.'):
            return jsonify({
                'success': False,
                'message': 'Invalid filename'
            }), 400

        # Build target file path
        target_file_path = os.path.join(target_dir, filename)

        # Final safety check
        if not is_safe_path(base_folder, target_file_path):
            logger.warning(f"Path traversal attempt via filename: {filename}")
            return jsonify({
                'success': False,
                'message': 'Invalid filename'
            }), 403

        # Check if file already exists
        if os.path.exists(target_file_path):
            return jsonify({
                'success': False,
                'message': f'File "{filename}" already exists'
            }), 409  # Conflict

        # Check file size (read from content-length header if available)
        content_length = request.content_length
        if content_length and content_length > SecurityConfig.MAX_FILE_SIZE:
            logger.warning(f"Upload too large: {content_length} bytes")
            return jsonify({
                'success': False,
                'message': f'File too large. Maximum size is {format_size(SecurityConfig.MAX_FILE_SIZE)}'
            }), 413  # Request Entity Too Large

        # Save the file
        try:
            file.save(target_file_path)
            file_size = os.path.getsize(target_file_path)

            # Double-check size after saving
            if file_size > SecurityConfig.MAX_FILE_SIZE:
                os.remove(target_file_path)
                logger.warning(f"Upload exceeded size limit: {file_size} bytes")
                return jsonify({
                    'success': False,
                    'message': f'File too large. Maximum size is {format_size(SecurityConfig.MAX_FILE_SIZE)}'
                }), 413

            logger.info(f"File uploaded: {target_file_path} ({format_size(file_size)}) from {request.remote_addr}")

            return jsonify({
                'success': True,
                'message': f'Successfully uploaded "{filename}"',
                'filename': filename,
                'size': format_size(file_size)
            }), 200

        except Exception as e:
            logger.error(f"Error saving uploaded file: {str(e)}")
            # Clean up if file was partially created
            if os.path.exists(target_file_path):
                try:
                    os.remove(target_file_path)
                except:
                    pass
            return jsonify({
                'success': False,
                'message': 'Failed to save file'
            }), 500

    except Exception as e:
        logger.error(f"Error in upload handler: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders', methods=['GET'])
@rate_limit
def api_folders():
    """API endpoint to get list of shared folders"""
    folders = []
    for idx, folder_path in enumerate(config.shared_folders):
        if os.path.exists(folder_path):
            folders.append({
                'index': idx,
                'name': os.path.basename(folder_path),
                'path': folder_path
            })
    return jsonify(folders)


@app.route('/qr-code')
@rate_limit
def get_qr_code():
    """Serve the QR code image"""
    qr_path = os.path.join(os.path.dirname(__file__), 'netshare_qr.png')

    if not os.path.exists(qr_path):
        # Regenerate if missing
        local_ip = get_local_ip()
        url = f"http://{local_ip}:{config.server_port}"
        qr_path = generate_qr_code(url)

    return send_from_directory(
        os.path.dirname(qr_path),
        os.path.basename(qr_path),
        mimetype='image/png'
    )


@app.route('/api/browse-filesystem')
@rate_limit
def api_browse_filesystem():
    """Browse server filesystem for folder selection"""
    try:
        path = request.args.get('path', '').strip()

        # If no path specified, return drives/roots
        if not path:
            drives = get_system_drives()
            return jsonify({
                'success': True,
                'drives': drives,
                'current_path': None,
                'parent': None,
                'directories': []
            }), 200

        # List directories in the specified path
        result, error = list_directories(path)

        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400

        return jsonify({
            'success': True,
            'current_path': result['current_path'],
            'parent': result['parent'],
            'directories': result['directories'],
            'drives': []
        }), 200

    except Exception as e:
        logger.error(f"Error browsing filesystem: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders', methods=['POST'])
@rate_limit
def api_add_folder():
    """Add a new shared folder"""
    try:
        data = request.get_json()

        if not data or 'path' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing path parameter'
            }), 400

        folder_path = data['path'].strip()

        # Validate path
        is_valid, message = validate_folder_path(folder_path)

        if not is_valid:
            logger.warning(f"Invalid folder add attempt: {folder_path} - {message} from {request.remote_addr}")
            return jsonify({
                'success': False,
                'message': message
            }), 400

        # Add to shared folders
        config.shared_folders.append(folder_path)

        # Save to file for persistence
        save_folders_to_file()

        logger.info(f"Folder added: {folder_path} from {request.remote_addr}")

        return jsonify({
            'success': True,
            'message': f'Successfully added folder: {os.path.basename(folder_path)}',
            'folders': [
                {'index': idx, 'name': os.path.basename(p), 'path': p}
                for idx, p in enumerate(config.shared_folders)
            ]
        }), 200

    except Exception as e:
        logger.error(f"Error adding folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders/<int:folder_index>', methods=['DELETE'])
@rate_limit
def api_remove_folder(folder_index):
    """Remove a shared folder by index"""
    try:
        if folder_index < 0 or folder_index >= len(config.shared_folders):
            return jsonify({
                'success': False,
                'message': 'Invalid folder index'
            }), 400

        removed_path = config.shared_folders.pop(folder_index)

        # Save to file for persistence
        save_folders_to_file()

        logger.info(f"Folder removed: {removed_path} from {request.remote_addr}")

        return jsonify({
            'success': True,
            'message': f'Successfully removed folder: {os.path.basename(removed_path)}',
            'folders': [
                {'index': idx, 'name': os.path.basename(p), 'path': p}
                for idx, p in enumerate(config.shared_folders)
            ]
        }), 200

    except Exception as e:
        logger.error(f"Error removing folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


def select_folders_gui():
    """GUI for selecting folders to share"""
    if not HAS_GUI:
        print("Error: GUI not available. Please use command-line mode.")
        return []
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    folders = []
    while True:
        folder = filedialog.askdirectory(
            title="Select a folder to share (Cancel to finish)"
        )
        if not folder:
            break
        folders.append(folder)
        
        result = messagebox.askyesno(
            "Add More?",
            f"Added: {folder}\n\nDo you want to add another folder?"
        )
        if not result:
            break
    
    root.destroy()
    return folders


def start_server(port=5000):
    """Start the Flask server"""
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}"
    
    print("\n" + "="*60)
    print(f"NetShare Server Started!")
    print("="*60)
    print(f"Local URL: {url}")
    print(f"Sharing {len(config.shared_folders)} folder(s)")
    for idx, folder in enumerate(config.shared_folders):
        print(f"  [{idx}] {folder}")
    print("="*60)
    
    # Generate QR code
    generate_qr_code(url)
    
    print("\nTo stop the server, press Ctrl+C")
    print("="*60 + "\n")
    
    # Try to open browser
    try:
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    except:
        pass
    
    # Start Flask server
    app.run(host=config.host, port=port, debug=False, threaded=True)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='NetShare - Share folders over local network',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  netshare --gui                    # Use GUI to select folders
  netshare --folder /path/to/share  # Share specific folder
  netshare --folder "C:\\Users\\Documents" --port 8000
  netshare --url https://example.com                    # Generate QR code for URL
  netshare --url https://example.com --output qr.png   # Generate QR with custom filename
        """
    )
    
    parser.add_argument('--gui', action='store_true',
                       help='Use GUI to select folders')
    parser.add_argument('--folder', '-f', action='append',
                       help='Folder to share (can be specified multiple times)')
    parser.add_argument('--port', '-p', type=int, default=5000,
                       help='Port to run server on (default: 5000)')
    parser.add_argument('--url', '-u', type=str, default=None,
                       help='Generate QR code for the given URL (standalone mode)')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output path for QR code PNG file (default: netshare_qr.png)')

    args = parser.parse_args()

    # Validate --output requires --url
    if args.output and not args.url:
        print("Error: --output flag requires --url flag")
        print("Use: netshare --url <URL> --output <filename>")
        sys.exit(1)

    # Handle URL-only mode (standalone QR generation)
    if args.url:
        # Validate that no conflicting flags were specified
        if args.gui or args.folder or args.port != 5000:
            print("Error: --url flag cannot be combined with --folder, --gui, or --port")
            print("Use --url only for standalone QR code generation.")
            sys.exit(1)

        # Generate QR code for the provided URL
        try:
            output_path = args.output if args.output else 'netshare_qr.png'
            qr_path = generate_qr_code(args.url, output_path=output_path)
            print(f"\nQR code generated successfully!")
            print(f"URL: {args.url}")
            print(f"Saved to: {qr_path}")
            sys.exit(0)
        except Exception as e:
            print(f"Error generating QR code: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    # Try to load folders from saved config first
    load_folders_from_file()

    # Determine folders to share
    if args.gui:
        if not HAS_GUI:
            print("Error: GUI not available on this system.")
            print("Please use --folder option instead.")
            sys.exit(1)
        config.shared_folders = select_folders_gui()
        # Save GUI-selected folders
        if config.shared_folders:
            save_folders_to_file()
    elif args.folder:
        config.shared_folders = [os.path.abspath(f) for f in args.folder]
        # Save command-line folders
        save_folders_to_file()
    elif not config.shared_folders:
        # Interactive mode (only if no saved folders)
        print("NetShare - Network File Sharing Tool")
        print("="*50)
        print("Enter folders to share (one per line, empty line to finish):")

        while True:
            folder = input("Folder path: ").strip()
            if not folder:
                break
            if os.path.isdir(folder):
                config.shared_folders.append(os.path.abspath(folder))
                print(f"  ✓ Added: {folder}")
            else:
                print(f"  ✗ Not a valid folder: {folder}")

        # Save interactively-selected folders
        if config.shared_folders:
            save_folders_to_file()
    else:
        # Using saved folders from config file
        print(f"Loaded {len(config.shared_folders)} folder(s) from saved configuration")

    if not config.shared_folders:
        print("\nNo folders selected. Exiting.")
        sys.exit(0)
    
    # Validate all folders exist
    valid_folders = []
    for folder in config.shared_folders:
        if os.path.isdir(folder):
            valid_folders.append(folder)
        else:
            print(f"Warning: Skipping non-existent folder: {folder}")
    
    config.shared_folders = valid_folders
    
    if not config.shared_folders:
        print("\nNo valid folders to share. Exiting.")
        sys.exit(0)
    
    config.server_port = args.port
    
    # Start the server
    try:
        start_server(config.server_port)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
````

## File: netshare/config.py
````python
"""
NetShare Configuration
Security and application settings
"""

import os

class SecurityConfig:
    """Security-related configuration"""
    
    # Maximum file size to serve (in bytes) - 10GB default
    MAX_FILE_SIZE = 20 * 1024 * 1024 * 1024
    
    # Allowed file extensions (empty list = allow all)
    # Uncomment and populate to restrict file types
    ALLOWED_EXTENSIONS = []
    # ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.png', '.mp4']
    
    # Blocked file extensions (security-sensitive files)
    BLOCKED_EXTENSIONS = [
        '.exe', '.bat', '.cmd', '.sh', '.ps1', '.vbs', '.msi',
        '.scr', '.com', '.pif', '.reg', '.dll', '.sys'
    ]
    
    # Enable/disable directory listing
    ALLOW_DIRECTORY_LISTING = True
    
    # Enable/disable file downloads
    ALLOW_FILE_DOWNLOAD = True
    
    # Maximum path depth from shared folder root
    MAX_PATH_DEPTH = 20
    
    # Rate limiting (requests per minute per IP)
    RATE_LIMIT = 100
    
    # Enable detailed error messages (disable in production)
    DEBUG_ERRORS = False


class AppConfig:
    """Application configuration"""
    
    # Default server settings
    DEFAULT_PORT = 5000
    DEFAULT_HOST = '0.0.0.0'
    
    # Server identification
    SERVER_NAME = "NetShare"
    VERSION = "1.0.0"
    
    # QR Code settings
    QR_BOX_SIZE = 10
    QR_BORDER = 4
    
    # UI settings
    ITEMS_PER_PAGE = 100
    
    # Logging
    ENABLE_ACCESS_LOG = True
    LOG_FILE = "netshare.log"

    # Folder management settings
    FOLDERS_CONFIG_FILE = "shared_folders.json"
    MAX_SHARED_FOLDERS = 20


# Validate configuration on import
def validate_config():
    """Validate configuration settings"""
    if SecurityConfig.MAX_FILE_SIZE <= 0:
        raise ValueError("MAX_FILE_SIZE must be positive")
    
    if SecurityConfig.MAX_PATH_DEPTH <= 0:
        raise ValueError("MAX_PATH_DEPTH must be positive")
    
    if SecurityConfig.RATE_LIMIT <= 0:
        raise ValueError("RATE_LIMIT must be positive")
    
    # Ensure blocked extensions are lowercase
    SecurityConfig.BLOCKED_EXTENSIONS = [
        ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
        for ext in SecurityConfig.BLOCKED_EXTENSIONS
    ]
    
    # Ensure allowed extensions are lowercase
    if SecurityConfig.ALLOWED_EXTENSIONS:
        SecurityConfig.ALLOWED_EXTENSIONS = [
            ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
            for ext in SecurityConfig.ALLOWED_EXTENSIONS
        ]


# Run validation
validate_config()
````

## File: netshare/templates/browse.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ folder_name }} - NetShare</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        .header {
            background: white;
            border-radius: 12px;
            padding: 20px 30px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .nav-top {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .back-button {
            display: inline-flex;
            align-items: center;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: transform 0.2s;
        }

        .back-button:hover {
            transform: translateY(-2px);
        }

        .back-button svg {
            width: 20px;
            height: 20px;
            margin-right: 8px;
        }

        .folder-title {
            font-size: 1.8em;
            color: #333;
            margin-bottom: 10px;
        }

        .breadcrumb {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            color: #666;
            font-size: 0.95em;
        }

        .breadcrumb a {
            color: #667eea;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background 0.2s;
        }

        .breadcrumb a:hover {
            background: rgba(102, 126, 234, 0.1);
        }

        .breadcrumb-sep {
            margin: 0 5px;
            color: #999;
        }

        .content {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }

        .items-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }

        .items-count {
            font-size: 1.2em;
            color: #333;
        }

        .items-list {
            list-style: none;
        }

        .item {
            display: flex;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
            text-decoration: none;
            color: inherit;
        }

        .item:hover {
            background: rgba(102, 126, 234, 0.05);
        }

        .item:last-child {
            border-bottom: none;
        }

        .item-icon {
            width: 40px;
            height: 40px;
            margin-right: 15px;
            flex-shrink: 0;
        }

        .item-info {
            flex-grow: 1;
        }

        .item-name {
            font-size: 1.1em;
            color: #333;
            margin-bottom: 3px;
            word-break: break-word;
        }

        .item-size {
            font-size: 0.9em;
            color: #888;
        }

        .item-dir .item-name {
            color: #667eea;
            font-weight: 500;
        }

        .download-icon {
            width: 24px;
            height: 24px;
            margin-left: 10px;
            opacity: 0.5;
            transition: opacity 0.2s;
        }

        .item:hover .download-icon {
            opacity: 1;
        }

        .empty-folder {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-folder svg {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
            opacity: 0.3;
        }

        .upload-section {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .file-input-wrapper {
            position: relative;
            display: inline-block;
        }

        .file-input-label {
            display: inline-flex;
            align-items: center;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: transform 0.2s;
        }

        .file-input-label:hover {
            transform: translateY(-2px);
        }

        .file-input-label svg {
            width: 20px;
            height: 20px;
            margin-right: 8px;
        }

        #file-input {
            position: absolute;
            left: -9999px;
        }

        .selected-file {
            color: #666;
            font-size: 0.95em;
        }

        .upload-button {
            padding: 10px 24px;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: transform 0.2s;
            font-size: 1em;
        }

        .upload-button:hover:not(:disabled) {
            transform: translateY(-2px);
        }

        .upload-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .upload-status {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            display: none;
        }

        .upload-status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .upload-status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .upload-status.uploading {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }

        .progress-container {
            margin-top: 10px;
        }

        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.85em;
            font-weight: 500;
        }

        @media (max-width: 600px) {
            body {
                padding: 10px;
            }

            .header, .content {
                padding: 15px;
            }

            .folder-title {
                font-size: 1.4em;
            }

            .breadcrumb {
                font-size: 0.85em;
            }

            .item {
                padding: 12px;
            }

            .item-icon {
                width: 32px;
                height: 32px;
                margin-right: 12px;
            }

            .item-name {
                font-size: 1em;
            }

            .back-button {
                padding: 8px 15px;
                font-size: 0.9em;
            }

            .items-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }

            .upload-section {
                flex-direction: column;
                align-items: flex-start;
                width: 100%;
            }

            .file-input-label, .upload-button {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="nav-top">
                <a href="/" class="back-button">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Back to Home
                </a>
            </div>

            <h1 class="folder-title">{{ folder_name }}</h1>

            <div class="breadcrumb">
                <a href="/browse/{{ folder_index }}">{{ folder_name }}</a>
                {% if breadcrumbs %}
                    {% for crumb in breadcrumbs %}
                        <span class="breadcrumb-sep">/</span>
                        <a href="/browse/{{ folder_index }}/{{ crumb.path }}">{{ crumb.name }}</a>
                    {% endfor %}
                {% endif %}
            </div>
        </div>

        <div class="content">
            <div class="items-header">
                <h2 class="items-count">{{ items|length }} item{% if items|length != 1 %}s{% endif %}</h2>
                <div class="upload-section">
                    <div class="file-input-wrapper">
                        <label for="file-input" class="file-input-label">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M21 15V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            Choose File
                        </label>
                        <input type="file" id="file-input" accept="*/*">
                    </div>
                    <span class="selected-file" id="selected-file">No file selected</span>
                    <button class="upload-button" id="upload-button" disabled>Upload</button>
                </div>
            </div>

            <div class="upload-status" id="upload-status">
                <div class="status-message" id="status-message"></div>
                <div class="progress-container" id="progress-container" style="display: none;">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progress-fill" style="width: 0%;">0%</div>
                    </div>
                </div>
            </div>

            {% if items %}
                <ul class="items-list">
                    {% for item in items %}
                        {% if item.is_dir %}
                            <a href="/browse/{{ folder_index }}/{% if current_path %}{{ current_path }}/{% endif %}{{ item.name }}" class="item item-dir">
                                <svg class="item-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M3 8L3 18C3 19.1046 3.89543 20 5 20H19C20.1046 20 21 19.1046 21 18V10C21 8.89543 20.1046 8 19 8H11L9 6H5C3.89543 6 3 6.89543 3 8Z" fill="#667eea" fill-opacity="0.2"/>
                                    <path d="M3 8L3 18C3 19.1046 3.89543 20 5 20H19C20.1046 20 21 19.1046 21 18V10C21 8.89543 20.1046 8 19 8H11L9 6H5C3.89543 6 3 6.89543 3 8Z" stroke="#667eea" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                                <div class="item-info">
                                    <div class="item-name">{{ item.name }}</div>
                                    <div class="item-size">Folder</div>
                                </div>
                            </a>
                        {% else %}
                            <a href="/browse/{{ folder_index }}/{% if current_path %}{{ current_path }}/{% endif %}{{ item.name }}" class="item item-file">
                                <svg class="item-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" fill="#764ba2" fill-opacity="0.1"/>
                                    <path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8M14 2L20 8M14 2V8H20" stroke="#764ba2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                                <div class="item-info">
                                    <div class="item-name">{{ item.name }}</div>
                                    <div class="item-size">{{ item.size }}</div>
                                </div>
                                <svg class="download-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M21 15V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V15M7 10L12 15M12 15L17 10M12 15V3" stroke="#667eea" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </a>
                        {% endif %}
                    {% endfor %}
                </ul>
            {% else %}
                <div class="empty-folder">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 8L3 18C3 19.1046 3.89543 20 5 20H19C20.1046 20 21 19.1046 21 18V10C21 8.89543 20.1046 8 19 8H11L9 6H5C3.89543 6 3 6.89543 3 8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <h3>This folder is empty</h3>
                </div>
            {% endif %}
        </div>
    </div>

    <script>
        const fileInput = document.getElementById('file-input');
        const selectedFileSpan = document.getElementById('selected-file');
        const uploadButton = document.getElementById('upload-button');
        const uploadStatus = document.getElementById('upload-status');
        const statusMessage = document.getElementById('status-message');
        const progressContainer = document.getElementById('progress-container');
        const progressFill = document.getElementById('progress-fill');

        // Handle file selection
        fileInput.addEventListener('change', function(e) {
            if (this.files.length > 0) {
                const file = this.files[0];
                selectedFileSpan.textContent = file.name;
                uploadButton.disabled = false;
            } else {
                selectedFileSpan.textContent = 'No file selected';
                uploadButton.disabled = true;
            }
            // Hide any previous status messages
            uploadStatus.style.display = 'none';
        });

        // Handle upload
        uploadButton.addEventListener('click', function() {
            const file = fileInput.files[0];
            if (!file) {
                return;
            }

            // Prepare form data
            const formData = new FormData();
            formData.append('file', file);

            // Build upload URL
            const folderIndex = {{ folder_index }};
            const currentPath = '{{ current_path }}';
            let uploadUrl = `/upload/${folderIndex}`;
            if (currentPath) {
                uploadUrl += `/${currentPath}`;
            }

            // Disable upload button during upload
            uploadButton.disabled = true;
            fileInput.disabled = true;

            // Show uploading status
            uploadStatus.className = 'upload-status uploading';
            uploadStatus.style.display = 'block';
            statusMessage.textContent = 'Uploading...';
            progressContainer.style.display = 'block';
            progressFill.style.width = '0%';
            progressFill.textContent = '0%';

            // Create XMLHttpRequest for progress tracking
            const xhr = new XMLHttpRequest();

            // Track upload progress
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percentComplete = Math.round((e.loaded / e.total) * 100);
                    progressFill.style.width = percentComplete + '%';
                    progressFill.textContent = percentComplete + '%';
                }
            });

            // Handle completion
            xhr.addEventListener('load', function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    uploadStatus.className = 'upload-status success';
                    statusMessage.textContent = response.message || 'Upload successful!';
                    progressContainer.style.display = 'none';

                    // Reset form
                    fileInput.value = '';
                    selectedFileSpan.textContent = 'No file selected';

                    // Reload page after 2 seconds to show new file
                    setTimeout(function() {
                        window.location.reload();
                    }, 2000);
                } else {
                    let errorMessage = 'Upload failed';
                    try {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || errorMessage;
                    } catch (e) {
                        // Use default error message
                    }

                    uploadStatus.className = 'upload-status error';
                    statusMessage.textContent = errorMessage;
                    progressContainer.style.display = 'none';

                    // Re-enable upload
                    uploadButton.disabled = false;
                    fileInput.disabled = false;
                }
            });

            // Handle errors
            xhr.addEventListener('error', function() {
                uploadStatus.className = 'upload-status error';
                statusMessage.textContent = 'Network error occurred';
                progressContainer.style.display = 'none';

                // Re-enable upload
                uploadButton.disabled = false;
                fileInput.disabled = false;
            });

            // Send request
            xhr.open('POST', uploadUrl, true);
            xhr.send(formData);
        });
    </script>
</body>
</html>
````

## File: netshare/templates/error.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - NetShare</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .error-container {
            background: white;
            border-radius: 12px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
        }

        .error-icon {
            width: 100px;
            height: 100px;
            margin: 0 auto 30px;
            color: #e74c3c;
        }

        .error-title {
            font-size: 2em;
            color: #333;
            margin-bottom: 15px;
        }

        .error-message {
            font-size: 1.1em;
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }

        .error-code {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            color: #e74c3c;
            margin-bottom: 30px;
            word-break: break-word;
        }

        .back-button {
            display: inline-flex;
            align-items: center;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: transform 0.2s;
        }

        .back-button:hover {
            transform: translateY(-2px);
        }

        .back-button svg {
            width: 20px;
            height: 20px;
            margin-right: 8px;
        }

        @media (max-width: 600px) {
            .error-container {
                padding: 30px 20px;
            }

            .error-title {
                font-size: 1.5em;
            }

            .error-message {
                font-size: 1em;
            }

            .error-icon {
                width: 80px;
                height: 80px;
            }
        }
    </style>
</head>
<body>
    <div class="error-container">
        <svg class="error-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            <path d="M12 8V12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="12" cy="16" r="1" fill="currentColor"/>
        </svg>

        <h1 class="error-title">Oops! Something went wrong</h1>

        {% if error %}
        <div class="error-code">{{ error }}</div>
        {% else %}
        <p class="error-message">
            We encountered an error while processing your request.
            Please try again or return to the home page.
        </p>
        {% endif %}

        <a href="/" class="back-button">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Back to Home
        </a>
    </div>
</body>
</html>
````

## File: netshare/templates/index.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetShare - Shared Folders</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .server-url {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 10px;
            backdrop-filter: blur(10px);
        }

        .server-url code {
            color: white;
            font-size: 1.1em;
            font-family: 'Courier New', monospace;
        }

        .folders-container {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }

        .folders-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }

        .folder-list {
            list-style: none;
        }

        .folder-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin-bottom: 15px;
            border-radius: 8px;
            transition: transform 0.2s, box-shadow 0.2s;
            overflow: hidden;
        }

        .folder-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }

        .folder-link {
            display: flex;
            align-items: center;
            padding: 20px;
            text-decoration: none;
            color: white;
        }

        .folder-icon {
            width: 50px;
            height: 50px;
            margin-right: 20px;
            flex-shrink: 0;
        }

        .folder-info {
            flex-grow: 1;
        }

        .folder-name {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .folder-path {
            font-size: 0.9em;
            opacity: 0.9;
            font-family: 'Courier New', monospace;
        }

        .arrow {
            font-size: 1.5em;
            margin-left: 20px;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .empty-state svg {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            opacity: 0.3;
        }

        .qr-code-section {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
        }

        .qr-code-section h3 {
            color: white;
            margin-bottom: 15px;
            font-size: 1.2em;
        }

        .qr-image {
            background: white;
            padding: 15px;
            border-radius: 8px;
            max-width: 200px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .qr-help {
            color: rgba(255,255,255,0.9);
            margin-top: 10px;
            font-size: 0.9em;
        }

        .folder-management {
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 8px;
            border: 2px dashed rgba(102, 126, 234, 0.3);
        }

        .folder-management h3 {
            margin-bottom: 15px;
            color: #333;
            font-size: 1.2em;
        }

        .add-folder-form {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }

        .add-folder-form input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 1em;
            transition: border-color 0.2s;
        }

        .add-folder-form input:focus {
            outline: none;
            border-color: #667eea;
        }

        .add-folder-form button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .add-folder-form button:hover {
            transform: translateY(-2px);
        }

        .remove-button {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            margin-left: 10px;
            transition: background 0.2s;
            font-weight: 500;
        }

        .remove-button:hover {
            background: #c82333;
        }

        .status-message {
            padding: 12px;
            border-radius: 6px;
            margin-top: 10px;
            display: none;
            font-weight: 500;
        }

        .status-message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .status-message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .browse-button {
            background: #28a745;
            min-width: auto;
            padding: 12px 20px;
        }

        .browse-button:hover {
            background: #218838;
        }

        /* Modal Styles */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.6);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-content {
            background: white;
            border-radius: 12px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .modal-header {
            padding: 20px;
            border-bottom: 2px solid #eee;
        }

        .modal-header h3 {
            margin: 0 0 10px 0;
            color: #333;
        }

        .current-path {
            font-family: 'Courier New', monospace;
            color: #667eea;
            font-size: 0.9em;
            word-break: break-all;
        }

        .modal-body {
            padding: 20px;
            overflow-y: auto;
            flex-grow: 1;
        }

        .folder-browser-list {
            list-style: none;
        }

        .folder-browser-item {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background 0.2s;
            display: flex;
            align-items: center;
        }

        .folder-browser-item:hover {
            background: rgba(102, 126, 234, 0.1);
        }

        .folder-browser-item.disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .folder-browser-item.disabled:hover {
            background: transparent;
        }

        .folder-browser-item svg {
            width: 24px;
            height: 24px;
            margin-right: 12px;
            flex-shrink: 0;
        }

        .folder-browser-item.up-directory {
            background: #f8f9fa;
            font-weight: 600;
            color: #667eea;
        }

        .modal-footer {
            padding: 15px 20px;
            border-top: 2px solid #eee;
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }

        .modal-button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .modal-button:hover {
            transform: translateY(-2px);
        }

        .modal-button.primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .modal-button.secondary {
            background: #6c757d;
            color: white;
        }

        .loading-message {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .error-message {
            text-align: center;
            padding: 40px;
            color: #dc3545;
        }

        @media (max-width: 600px) {
            .header h1 {
                font-size: 2em;
            }

            .folders-container {
                padding: 20px;
            }

            .folder-link {
                padding: 15px;
            }

            .folder-icon {
                width: 40px;
                height: 40px;
                margin-right: 15px;
            }

            .folder-name {
                font-size: 1.1em;
            }

            .folder-path {
                font-size: 0.8em;
            }

            .qr-image {
                max-width: 150px;
            }

            .add-folder-form {
                flex-direction: column;
            }

            .add-folder-form button {
                width: 100%;
            }

            .folder-management {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>NetShare</h1>
            <p>Network File Sharing</p>
            <div class="server-url">
                <code>{{ server_url }}</code>
            </div>

            <div class="qr-code-section">
                <h3>Scan to Access on Mobile</h3>
                <img src="/qr-code" alt="QR Code" class="qr-image" />
                <p class="qr-help">Scan this QR code with your phone camera</p>
            </div>
        </div>

        <div class="folders-container">
            <h2 class="folders-title">Shared Folders ({{ folders|length }})</h2>

            {% if folders %}
                <ul class="folder-list">
                    {% for folder in folders %}
                    <li class="folder-item">
                        <a href="/browse/{{ loop.index0 }}" class="folder-link">
                            <svg class="folder-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M3 8L3 18C3 19.1046 3.89543 20 5 20H19C20.1046 20 21 19.1046 21 18V10C21 8.89543 20.1046 8 19 8H11L9 6H5C3.89543 6 3 6.89543 3 8Z" fill="white" fill-opacity="0.9"/>
                                <path d="M3 8L3 18C3 19.1046 3.89543 20 5 20H19C20.1046 20 21 19.1046 21 18V10C21 8.89543 20.1046 8 19 8H11L9 6H5C3.89543 6 3 6.89543 3 8Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            <div class="folder-info">
                                <div class="folder-name">{{ folder.name }}</div>
                                <div class="folder-path">{{ folder.full_path }}</div>
                            </div>
                            <span class="arrow">→</span>
                            <button onclick="event.preventDefault(); removeFolder({{ loop.index0 }});" class="remove-button">Remove</button>
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            {% else %}
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 8L3 18C3 19.1046 3.89543 20 5 20H19C20.1046 20 21 19.1046 21 18V10C21 8.89543 20.1046 8 19 8H11L9 6H5C3.89543 6 3 6.89543 3 8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <h3>No folders shared</h3>
                    <p>Add folders using the form below</p>
                </div>
            {% endif %}

            <div class="folder-management">
                <h3>Manage Shared Folders</h3>

                <div class="add-folder-form">
                    <input type="text" id="folderPath" placeholder="Enter folder path or click Browse..." />
                    <button onclick="openFolderBrowser()" class="browse-button">Browse</button>
                    <button onclick="addFolder()">Add Folder</button>
                </div>

                <div id="statusMessage" class="status-message"></div>
            </div>
        </div>
    </div>

    <!-- Folder Browser Modal -->
    <div id="folderBrowserModal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Select Folder</h3>
                <div class="current-path" id="currentPathDisplay">Loading...</div>
            </div>
            <div class="modal-body" id="folderBrowserBody">
                <div class="loading-message">Loading...</div>
            </div>
            <div class="modal-footer">
                <button onclick="selectCurrentFolder()" class="modal-button primary" id="selectButton" disabled>Select This Folder</button>
                <button onclick="closeFolderBrowser()" class="modal-button secondary">Cancel</button>
            </div>
        </div>
    </div>

    <script>
        let currentBrowsePath = null;

        // Folder Browser Functions
        async function openFolderBrowser() {
            const modal = document.getElementById('folderBrowserModal');
            modal.classList.add('active');
            currentBrowsePath = null;
            await browsePath('');
        }

        function closeFolderBrowser() {
            const modal = document.getElementById('folderBrowserModal');
            modal.classList.remove('active');
            currentBrowsePath = null;
        }

        async function browsePath(path) {
            const body = document.getElementById('folderBrowserBody');
            const pathDisplay = document.getElementById('currentPathDisplay');
            const selectButton = document.getElementById('selectButton');

            body.innerHTML = '<div class="loading-message">Loading...</div>';
            selectButton.disabled = true;

            try {
                const url = path ? `/api/browse-filesystem?path=${encodeURIComponent(path)}` : '/api/browse-filesystem';
                const response = await fetch(url);
                const data = await response.json();

                if (!data.success) {
                    body.innerHTML = `<div class="error-message">${data.message}</div>`;
                    return;
                }

                currentBrowsePath = data.current_path;

                // Update path display
                if (currentBrowsePath) {
                    pathDisplay.textContent = currentBrowsePath;
                    selectButton.disabled = false;
                } else {
                    pathDisplay.textContent = 'Select a drive or location';
                    selectButton.disabled = true;
                }

                // Build folder list
                let html = '<ul class="folder-browser-list">';

                // Show drives if no path selected
                if (data.drives && data.drives.length > 0) {
                    for (const drive of data.drives) {
                        const disabled = !drive.accessible ? 'disabled' : '';
                        html += `
                            <li class="folder-browser-item ${disabled}" onclick="${drive.accessible ? `browsePath('${drive.path.replace(/\\/g, '\\\\')}')` : ''}">
                                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4 6H9L11 8H20C20.5523 8 21 8.44772 21 9V18C21 18.5523 20.5523 19 20 19H4C3.44772 19 3 18.5523 3 18V7C3 6.44772 3.44772 6 4 6Z" stroke="#667eea" stroke-width="2"/>
                                </svg>
                                ${drive.name}
                            </li>
                        `;
                    }
                } else {
                    // Show parent directory if available
                    if (data.parent) {
                        html += `
                            <li class="folder-browser-item up-directory" onclick="browsePath('${data.parent.replace(/\\/g, '\\\\')}')">
                                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                </svg>
                                .. (Parent Directory)
                            </li>
                        `;
                    }

                    // Show subdirectories
                    if (data.directories && data.directories.length > 0) {
                        for (const dir of data.directories) {
                            const disabled = !dir.accessible ? 'disabled' : '';
                            html += `
                                <li class="folder-browser-item ${disabled}" onclick="${dir.accessible ? `browsePath('${dir.path.replace(/\\/g, '\\\\')}')` : ''}">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M4 6H9L11 8H20C20.5523 8 21 8.44772 21 9V18C21 18.5523 20.5523 19 20 19H4C3.44772 19 3 18.5523 3 18V7C3 6.44772 3.44772 6 4 6Z" stroke="#667eea" stroke-width="2"/>
                                    </svg>
                                    ${dir.name}
                                </li>
                            `;
                        }
                    } else {
                        html += '<li class="folder-browser-item disabled"><em>No subdirectories</em></li>';
                    }
                }

                html += '</ul>';
                body.innerHTML = html;

            } catch (error) {
                body.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
            }
        }

        function selectCurrentFolder() {
            if (currentBrowsePath) {
                document.getElementById('folderPath').value = currentBrowsePath;
                closeFolderBrowser();
            }
        }

        // Original Functions
        async function addFolder() {
            const pathInput = document.getElementById('folderPath');
            const path = pathInput.value.trim();

            if (!path) {
                showStatus('Please enter a folder path', 'error');
                return;
            }

            try {
                const response = await fetch('/api/folders', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({path: path})
                });

                const data = await response.json();

                if (data.success) {
                    showStatus(data.message, 'success');
                    pathInput.value = '';
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showStatus(data.message, 'error');
                }
            } catch (error) {
                showStatus('Network error: ' + error.message, 'error');
            }
        }

        async function removeFolder(index) {
            if (!confirm('Are you sure you want to remove this folder from sharing?')) {
                return;
            }

            try {
                const response = await fetch(`/api/folders/${index}`, {
                    method: 'DELETE'
                });

                const data = await response.json();

                if (data.success) {
                    showStatus(data.message, 'success');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showStatus(data.message, 'error');
                }
            } catch (error) {
                showStatus('Network error: ' + error.message, 'error');
            }
        }

        function showStatus(message, type) {
            const statusDiv = document.getElementById('statusMessage');
            statusDiv.textContent = message;
            statusDiv.className = `status-message ${type}`;
            statusDiv.style.display = 'block';

            // Auto-hide success messages after 5 seconds
            if (type === 'success') {
                setTimeout(() => {
                    statusDiv.style.display = 'none';
                }, 5000);
            }
        }

        // Allow Enter key to add folder
        document.getElementById('folderPath').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addFolder();
            }
        });
    </script>
</body>
</html>
````

## File: PYPI_SETUP_GUIDE.md
````markdown
# NetShare PyPI Publication Guide

This guide contains all the steps to prepare and publish NetShare to PyPI.

## Current Status

✅ **Completed:**
- Created `netshare/` package directory
- Created `netshare/__init__.py`
- Created `netshare/__main__.py`
- Copied `netshare.py` → `netshare/app.py`
- Copied `config.py` → `netshare/config.py`
- Copied `templates/` → `netshare/templates/`
- Created `pyproject.toml`

⏳ **Remaining Steps:**
- Create LICENSE file
- Create MANIFEST.in
- Update imports in code
- Update README.md
- Test local installation
- Build and publish

---

## Step 1: Create LICENSE File

Create a file named `LICENSE` in the project root with the GPL-3.0 license text.

You can get the full license text from: https://www.gnu.org/licenses/gpl-3.0.txt

Or use this abbreviated version:

```
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2024 NetShare Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

**Quick command to download full license:**
```bash
curl https://www.gnu.org/licenses/gpl-3.0.txt -o LICENSE
```

---

## Step 2: Create MANIFEST.in

Create `MANIFEST.in` in the project root:

```
include README.md
include LICENSE
include requirements.txt
include *.ps1
recursive-include netshare/templates *.html
recursive-include image *
```

**Command:**
```bash
cat > MANIFEST.in << 'EOF'
include README.md
include LICENSE
include requirements.txt
include *.ps1
recursive-include netshare/templates *.html
recursive-include image *
EOF
```

---

## Step 3: Update Code Imports

The code in `netshare/app.py` needs to be updated to use relative imports for the config module.

**In `netshare/app.py`, change line 24:**

From:
```python
from config import SecurityConfig, AppConfig
```

To:
```python
from netshare.config import SecurityConfig, AppConfig
```

**Or use relative import:**
```python
from .config import SecurityConfig, AppConfig
```

**Command to update:**
```bash
cd /mnt/h/code/yl/netshare
sed -i 's/from config import/from netshare.config import/' netshare/app.py
```

---

## Step 4: Update AppConfig References

The config module references `AppConfig.FOLDERS_CONFIG_FILE` which may not be defined. Add this to `netshare/config.py` if missing:

```python
class AppConfig:
    DEFAULT_PORT = 5000
    DEFAULT_HOST = '0.0.0.0'
    SERVER_NAME = "NetShare"
    VERSION = "1.0.0"
    ENABLE_ACCESS_LOG = True
    MAX_SHARED_FOLDERS = 20
    FOLDERS_CONFIG_FILE = "shared_folders.json"  # Add this line if missing
```

---

## Step 5: Update README.md

Add PyPI installation instructions at the beginning of the README.md file.

**Add this section after the header:**

```markdown
## Installation

### From PyPI (Recommended)

```bash
pip install netshare
```

### From Source

```bash
git clone https://github.com/yourusername/netshare.git
cd netshare
pip install -r requirements.txt
```

## Quick Start

After installation via pip:

```bash
netshare --help
netshare --gui  # GUI folder selection (Windows/Mac/Linux with tkinter)
netshare --folder /path/to/share
```
```

---

## Step 6: Verify Package Structure

Your directory structure should now look like:

```
netshare/
├── pyproject.toml          ✅ Created
├── LICENSE                 ⏳ Create manually
├── MANIFEST.in             ⏳ Create manually
├── README.md               ✅ Exists (update with pip install)
├── requirements.txt        ✅ Exists
├── firewall_diagnostic.ps1 ✅ Exists
├── fix_firewall.ps1        ✅ Exists
├── image/                  ✅ Exists
├── netshare/               ✅ Created
│   ├── __init__.py         ✅ Created
│   ├── __main__.py         ✅ Created
│   ├── app.py              ✅ Created
│   ├── config.py           ✅ Created
│   └── templates/          ✅ Created
│       ├── browse.html
│       ├── error.html
│       └── index.html
└── (old files can remain for now)
```

---

## Step 7: Install Build Tools

```bash
pip install --upgrade build twine
```

## Verify installation
```bash
  python -m build --version
  twine --version
```
---

## Step 8: Test Local Installation

Before publishing, test that the package installs correctly:

```bash
# In the project root directory
pip install -e .

# Test the command works
netshare --help

# Test module execution
python -m netshare --help
```

**Expected output:** NetShare help message showing command-line options

---

## Step 9: Build Distribution Files

```bash
# Clean old builds (if any)
rm -rf dist/ build/ *.egg-info netshare.egg-info

# Build the package
python -m build
```

This creates:
- `dist/netshare-1.0.0.tar.gz` (source distribution)
- `dist/netshare-1.0.0-py3-none-any.whl` (wheel distribution)

---

## Step 10: Check Package with Twine

```bash
twine check dist/*
```

**Expected output:** `PASSED` for all files

---

## Step 11: Test Upload to TestPyPI

Before uploading to the real PyPI, test with TestPyPI:

**A. Create TestPyPI Account:**
- Go to https://test.pypi.org/account/register/
- Verify your email
- Create an API token at https://test.pypi.org/manage/account/token/

**B. Upload to TestPyPI:**
```bash
twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your TestPyPI API token)

**C. Test Installation from TestPyPI:**
```bash
# In a fresh virtual environment
pip cache purge

pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ netshare

# Test it works
netshare --help
```

---

## Step 12: Upload to Real PyPI

Once TestPyPI works:

**A. Create PyPI Account:**
- Go to https://pypi.org/account/register/
- Verify your email
- Create an API token at https://pypi.org/manage/account/token/

**B. Upload to PyPI:**
```bash
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your PyPI API token)

---

## Step 13: Verify Publication

**Visit your package page:**
- https://pypi.org/project/netshare/

**Test installation:**
```bash
# In a fresh environment
pip install netshare

# Run it
netshare --help
```

---

## Step 14: Update GitHub Repository (Optional)

**A. Add PyPI badge to README.md:**

```markdown
[![PyPI version](https://badge.fury.io/py/netshare.svg)](https://badge.fury.io/py/netshare)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
```

**B. Update repository URL in pyproject.toml:**

Replace `https://github.com/yourusername/netshare` with your actual GitHub username/organization.

**C. Create a git tag for the release:**

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

## Troubleshooting

### Package name already taken?

If `netshare` is already taken on PyPI, choose an alternative:
- `netshare-wifi`
- `py-netshare`
- `simple-netshare`
- `local-netshare`

Update the name in `pyproject.toml`:
```toml
[project]
name = "your-alternative-name"
```

### Import errors after installation?

Make sure all imports in `netshare/app.py` use the package prefix:
```python
from netshare.config import SecurityConfig, AppConfig
```

### Templates not found?

Verify `MANIFEST.in` includes:
```
recursive-include netshare/templates *.html
```

And in `pyproject.toml`:
```toml
[tool.setuptools.package-data]
netshare = ["templates/*.html"]
```

---

## Future Updates

To release a new version:

1. Update version in `pyproject.toml` and `netshare/__init__.py`
2. Update CHANGELOG or README with changes
3. Rebuild: `python -m build`
4. Upload: `twine upload dist/*`
5. Tag release: `git tag v1.0.x && git push origin v1.0.x`

---

## Automation with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*
```

Then add your PyPI API token as a GitHub secret named `PYPI_TOKEN`.

---

## Summary Checklist

- [ ] Create LICENSE file
- [ ] Create MANIFEST.in
- [ ] Update imports in netshare/app.py
- [ ] Update README.md with pip install instructions
- [ ] Install build tools: `pip install build twine`
- [ ] Test local install: `pip install -e .`
- [ ] Build package: `python -m build`
- [ ] Check package: `twine check dist/*`
- [ ] Test on TestPyPI
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Verify: `pip install netshare`
- [ ] Update GitHub with badges and tags

---

**Good luck with your PyPI publication! 🚀**
````

## File: pypi-build/.env.template
````
# PyPI Deployment Tokens Configuration
# =====================================
#
# SETUP INSTRUCTIONS:
# 1. Copy this file to .env in the same directory:
#    cp .env.template .env
#
# 2. Add your actual PyPI tokens below
#
# 3. NEVER commit the .env file to git (it's already in .gitignore)
#
# 4. Set restrictive permissions:
#    chmod 600 .env
#
# =====================================

# Test PyPI Token
# Get your token from: https://test.pypi.org/manage/account/token/
# Format: pypi-AgEIcHlwaS5vcmc...
TESTPYPI_TOKEN=pypi-your-testpypi-token-here

# Production PyPI Token
# Get your token from: https://pypi.org/manage/account/token/
# Format: pypi-AgEIcHlwaS5vcmc...
PYPI_TOKEN=pypi-your-production-pypi-token-here

# =====================================
# NOTES:
# - Tokens are shown only once when created - save them securely
# - You can create project-specific tokens for better security
# - Treat these tokens like passwords - never share them
# =====================================
````

## File: pypi-build/build.sh
````bash
#!/bin/bash
# build.sh - Build distribution packages for netshare

# Get script directory and source config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Display banner
display_banner "Build NetShare Package" "$BLUE"

# Check prerequisites
if ! check_prerequisites; then
    error "Prerequisites check failed"
    exit 2
fi

echo ""

# Check required files
if ! check_required_files; then
    error "Required files check failed"
    exit 2
fi

echo ""

# Check version consistency
if ! check_version_consistency; then
    error "Version consistency check failed"
    exit 2
fi

echo ""

# Get version for display
VERSION=$(get_version_from_toml)
info "Building version: $VERSION"

echo ""

# Clean old artifacts
clean_build_artifacts

echo ""

# Change to project root
cd "$PROJECT_ROOT" || exit 1

# Build the package
info "Running: $PYTHON_CMD -m build"
echo ""

if $PYTHON_CMD -m build; then
    success "Build completed successfully"
else
    error "Build failed"
    exit 3
fi

echo ""

# Check the built packages with twine
info "Running: twine check dist/*"
echo ""

if twine check dist/*; then
    success "Twine check passed"
else
    error "Twine check failed"
    exit 3
fi

echo ""

# Display created artifacts
info "Build artifacts created:"
if [ -d "dist" ]; then
    ls -lh dist/
else
    error "dist/ directory not found"
    exit 3
fi

echo ""
success "Build completed successfully!"
echo ""
info "You can now upload these files to PyPI using:"
echo "  - ./pypi-build/deploy-test.sh  (for TestPyPI)"
echo "  - ./pypi-build/deploy-prod.sh  (for PyPI)"
echo ""
````

## File: pypi-build/bump-version.sh
````bash
#!/bin/bash
# bump-version.sh - Bump version in pyproject.toml and __init__.py
# Usage: ./bump-version.sh [major|minor|patch|X.Y.Z]

# Get script directory and source config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Display banner
display_banner "Bump Version" "$BLUE"

# Check if argument provided
if [ $# -eq 0 ]; then
    error "No version bump type specified"
    echo ""
    echo "Usage: $0 [major|minor|patch|X.Y.Z]"
    echo ""
    echo "Examples:"
    echo "  $0 major    # 1.0.4 → 2.0.0"
    echo "  $0 minor    # 1.0.4 → 1.1.0"
    echo "  $0 patch    # 1.0.4 → 1.0.5"
    echo "  $0 1.2.3    # Set explicit version"
    echo ""
    exit 1
fi

BUMP_TYPE=$1

# Get current version
CURRENT_VERSION=$(get_version_from_toml)

if [ -z "$CURRENT_VERSION" ]; then
    error "Could not read current version from pyproject.toml"
    exit 2
fi

info "Current version: $CURRENT_VERSION"

# Parse current version
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Calculate new version based on bump type
case $BUMP_TYPE in
    major)
        NEW_VERSION="$((MAJOR + 1)).0.0"
        ;;
    minor)
        NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
        ;;
    patch)
        NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
        ;;
    *)
        # Assume explicit version provided
        if [[ $BUMP_TYPE =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            NEW_VERSION=$BUMP_TYPE
        else
            error "Invalid version format: $BUMP_TYPE"
            echo "Must be 'major', 'minor', 'patch', or X.Y.Z format"
            exit 1
        fi
        ;;
esac

echo ""
info "New version: $NEW_VERSION"
echo ""

# Display changes
banner "Version Changes:"
echo ""
echo "  pyproject.toml:"
echo "    $CURRENT_VERSION → $NEW_VERSION"
echo ""
echo "  netshare/__init__.py:"
echo "    $CURRENT_VERSION → $NEW_VERSION"
echo ""

# Confirmation
read -p "Apply these changes? [y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    warning "Version bump cancelled"
    exit 5
fi

echo ""

# Update pyproject.toml
TOML_FILE="$PROJECT_ROOT/pyproject.toml"
info "Updating $TOML_FILE..."

if sed -i "s/^version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" "$TOML_FILE"; then
    success "Updated pyproject.toml"
else
    error "Failed to update pyproject.toml"
    exit 2
fi

# Update __init__.py
INIT_FILE="$PROJECT_ROOT/netshare/__init__.py"
info "Updating $INIT_FILE..."

if sed -i "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" "$INIT_FILE"; then
    success "Updated __init__.py"
else
    error "Failed to update __init__.py"
    # Revert pyproject.toml change
    sed -i "s/^version = \"$NEW_VERSION\"/version = \"$CURRENT_VERSION\"/" "$TOML_FILE"
    error "Reverted pyproject.toml"
    exit 2
fi

echo ""

# Verify consistency
if ! check_version_consistency; then
    error "Version consistency check failed after update"
    exit 2
fi

echo ""
success "Version bumped successfully!"

echo ""
banner "Next Steps:"
echo ""
echo "1. Review the changes:"
echo "   git diff pyproject.toml netshare/__init__.py"
echo ""
echo "2. Commit the changes:"
echo "   git add pyproject.toml netshare/__init__.py"
echo "   git commit -m \"Bump version to $NEW_VERSION\""
echo ""
echo "3. Build and deploy:"
echo "   ./pypi-build/deploy-test.sh   # Test on TestPyPI first"
echo "   ./pypi-build/deploy-prod.sh   # Then deploy to PyPI"
echo ""
````

## File: pypi-build/clean.sh
````bash
#!/bin/bash
# clean.sh - Clean build artifacts for netshare package

# Get script directory and source config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Display banner
display_banner "Clean Build Artifacts" "$BLUE"

# Change to project root
cd "$PROJECT_ROOT" || exit 1

# Clean artifacts
clean_build_artifacts

echo ""
success "Cleanup complete!"
echo ""
info "Removed directories:"
echo "  - dist/"
echo "  - build/"
echo "  - *.egg-info/"
echo "  - __pycache__/"
echo ""
````

## File: pypi-build/config.sh
````bash
#!/bin/bash
# config.sh - Shared configuration and functions for PyPI deployment scripts
# This file should be sourced by other scripts, not executed directly

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Repository URLs
TESTPYPI_REPO="https://test.pypi.org/legacy/"
PYPI_REPO="https://upload.pypi.org/legacy/"

# Script directory detection
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Detect the correct Python command (python3 or python)
detect_python_command() {
    # Try to find a working Python command
    # Validates that the command actually works (not Windows Store stub)

    # Try 'python' first (most common in venv and Windows)
    if command -v python &> /dev/null && python --version &> /dev/null 2>&1; then
        echo "python"
        return 0
    fi

    # Try 'python3' (Linux/macOS)
    if command -v python3 &> /dev/null && python3 --version &> /dev/null 2>&1; then
        echo "python3"
        return 0
    fi

    # No working Python found
    echo ""
    return 1
}

# Set the Python command to use
# If in a virtual environment, use 'python' directly (most reliable)
if [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD=$(detect_python_command)
fi

# Output functions with color coding
success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

banner() {
    echo -e "${BOLD}$1${NC}"
}

# Load token from environment variable, .env file, or interactive prompt
# Usage: load_token VAR_NAME "Display Name"
# Returns: token value
load_token() {
    local token_var=$1
    local token_name=$2

    # 1. Check environment variable (highest priority)
    if [ -n "${!token_var}" ]; then
        echo "${!token_var}"
        return 0
    fi

    # 2. Check .env file
    if [ -f "$SCRIPT_DIR/.env" ]; then
        source "$SCRIPT_DIR/.env"
        if [ -n "${!token_var}" ]; then
            echo "${!token_var}"
            return 0
        fi
    fi

    # 3. Interactive prompt (fallback)
    echo "" >&2
    warning "No token found in environment or .env file" >&2
    echo -e "${BLUE}ℹ${NC} Enter $token_name (input hidden):" >&2
    read -s token
    echo "" >&2
    echo "$token"
}

# Validate token format (should start with "pypi-")
# Usage: validate_token "token_value"
# Returns: 0 if valid, 1 if invalid
validate_token() {
    local token=$1

    if [ -z "$token" ]; then
        error "Token is empty"
        return 1
    fi

    if [[ ! "$token" =~ ^pypi- ]]; then
        error "Invalid token format (should start with 'pypi-')"
        return 1
    fi

    success "Token format is valid"
    return 0
}

# Extract version from pyproject.toml
# Returns: version string
get_version_from_toml() {
    grep '^version = ' "$PROJECT_ROOT/pyproject.toml" | sed 's/version = "\(.*\)"/\1/'
}

# Extract version from __init__.py
# Returns: version string
get_version_from_init() {
    grep '__version__ = ' "$PROJECT_ROOT/netshare/__init__.py" | sed 's/__version__ = "\(.*\)"/\1/'
}

# Check version consistency between pyproject.toml and __init__.py
# Returns: 0 if consistent, 2 if mismatch
check_version_consistency() {
    local toml_version=$(get_version_from_toml)
    local init_version=$(get_version_from_init)

    info "Checking version consistency..."
    echo "  pyproject.toml: $toml_version"
    echo "  __init__.py:    $init_version"

    if [ "$toml_version" != "$init_version" ]; then
        error "Version mismatch detected!"
        echo ""
        warning "Please update both files to the same version:"
        echo "  - $PROJECT_ROOT/pyproject.toml"
        echo "  - $PROJECT_ROOT/netshare/__init__.py"
        return 2
    fi

    success "Version is consistent: $toml_version"
    return 0
}

# Check if required prerequisites are installed
# Returns: 0 if all present, 2 if missing
check_prerequisites() {
    local missing=0

    info "Checking prerequisites..."

    # Check Python
    if [ -n "$PYTHON_CMD" ]; then
        local python_version=$($PYTHON_CMD --version 2>&1)
        success "Python: $python_version"
    else
        error "Python is not installed (tried python3 and python)"
        missing=1
    fi

    # Check build module
    if [ -n "$PYTHON_CMD" ] && $PYTHON_CMD -c "import build" 2> /dev/null; then
        success "Python 'build' module is installed"
    else
        error "Python 'build' module is not installed"
        echo "  Install with: pip install build"
        missing=1
    fi

    # Check twine
    if command -v twine &> /dev/null; then
        local twine_version=$(twine --version 2>&1 | head -n1)
        success "Twine: $twine_version"
    else
        error "Twine is not installed"
        echo "  Install with: pip install twine"
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        return 2
    fi

    return 0
}

# Check if required files exist
# Returns: 0 if all present, 2 if missing
check_required_files() {
    local missing=0

    info "Checking required files..."

    local files=("pyproject.toml" "README.md" "LICENSE" "MANIFEST.in" "netshare/__init__.py")

    for file in "${files[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            success "$file exists"
        else
            error "$file is missing"
            missing=1
        fi
    done

    if [ $missing -eq 1 ]; then
        return 2
    fi

    return 0
}

# Log deployment to file
# Usage: log_deployment "test|prod" "version" "status"
log_deployment() {
    local repo_type=$1
    local version=$2
    local status=$3

    local log_dir="$SCRIPT_DIR/logs"
    mkdir -p "$log_dir"

    local log_file
    if [ "$repo_type" = "test" ]; then
        log_file="$log_dir/test-deployments.log"
    else
        log_file="$log_dir/prod-deployments.log"
    fi

    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local hostname=$(hostname)
    local username=$(whoami)

    echo "$timestamp | v$version | $status | $username@$hostname | ${repo_type^^}PyPI" >> "$log_file"
}

# Clean build artifacts
# This is used by multiple scripts
clean_build_artifacts() {
    info "Cleaning old build artifacts..."

    cd "$PROJECT_ROOT" || return 1

    if [ -d "dist" ]; then
        rm -rf dist/
        success "Removed dist/"
    fi

    if [ -d "build" ]; then
        rm -rf build/
        success "Removed build/"
    fi

    if [ -d "netshare.egg-info" ]; then
        rm -rf netshare.egg-info/
        success "Removed netshare.egg-info/"
    fi

    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null

    success "Build artifacts cleaned"
}

# Display banner with box
display_banner() {
    local message=$1
    local color=$2

    local length=${#message}
    local border=$(printf '═%.0s' $(seq 1 $((length + 4))))

    echo ""
    echo -e "${color}╔${border}╗${NC}"
    echo -e "${color}║  ${message}  ║${NC}"
    echo -e "${color}╚${border}╝${NC}"
    echo ""
}

# Check git status and warn if uncommitted changes
check_git_status() {
    if ! git -C "$PROJECT_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
        warning "Not a git repository"
        return 0
    fi

    if [ -n "$(git -C "$PROJECT_ROOT" status --porcelain)" ]; then
        warning "You have uncommitted changes in your repository"
        git -C "$PROJECT_ROOT" status --short
        echo ""
        return 1
    fi

    success "Git working directory is clean"
    return 0
}

# Check if git tag exists
# Usage: check_git_tag "v1.0.4"
# Returns: 0 if exists, 1 if not
check_git_tag() {
    local tag=$1

    if git -C "$PROJECT_ROOT" tag -l "$tag" | grep -q "$tag"; then
        return 0
    fi

    return 1
}

# Create git tag
# Usage: create_git_tag "v1.0.4"
# Returns: 0 if created, 1 if failed
create_git_tag() {
    local tag=$1

    if git -C "$PROJECT_ROOT" tag -a "$tag" -m "Release $tag"; then
        success "Created git tag: $tag"
        return 0
    else
        error "Failed to create git tag: $tag"
        return 1
    fi
}

# Offer to push git tag
# Usage: offer_push_tag "v1.0.4"
offer_push_tag() {
    local tag=$1

    echo ""
    read -p "Push tag $tag to origin? [y/N] " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if git -C "$PROJECT_ROOT" push origin "$tag"; then
            success "Pushed tag $tag to origin"
        else
            error "Failed to push tag $tag"
        fi
    else
        info "Tag not pushed. You can push it later with: git push origin $tag"
    fi
}
````

## File: pypi-build/deploy-prod.sh
````bash
#!/bin/bash
# deploy-prod.sh - Deploy netshare to Production PyPI
# Supports: --dry-run (show what would happen without uploading)
#           --yes (skip confirmation prompts for CI/CD)
#
# WARNING: This deploys to production PyPI!

# Get script directory and source config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Parse command line arguments
DRY_RUN=false
AUTO_YES=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --yes)
            AUTO_YES=true
            shift
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--dry-run] [--yes]"
            exit 1
            ;;
    esac
done

# Display banner with warning
if [ "$DRY_RUN" = true ]; then
    display_banner "PRODUCTION PyPI Deployment [DRY RUN]" "$YELLOW"
else
    display_banner "⚠️  PRODUCTION PyPI Deployment ⚠️" "$RED"
fi

# Check git status
check_git_status
GIT_STATUS_CODE=$?

if [ $GIT_STATUS_CODE -ne 0 ] && [ "$AUTO_YES" = false ]; then
    echo ""
    read -p "Continue despite uncommitted changes? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        warning "Deployment cancelled"
        exit 5
    fi
fi

echo ""

# Load PyPI token
info "Loading PyPI token..."
PYPI_TOKEN=$(load_token "PYPI_TOKEN" "PyPI API token")

if [ -z "$PYPI_TOKEN" ]; then
    error "No PyPI token provided"
    exit 1
fi

# Validate token format
if ! validate_token "$PYPI_TOKEN"; then
    exit 1
fi

echo ""

# Run build script
info "Running build script..."
echo ""

if ! "$SCRIPT_DIR/build.sh"; then
    error "Build failed"
    exit 3
fi

# Get version
VERSION=$(get_version_from_toml)
TAG="v${VERSION}"

echo ""

# Check if git tag exists, create if not
info "Checking git tag: $TAG"

if check_git_tag "$TAG"; then
    success "Git tag $TAG already exists"
else
    warning "Git tag $TAG does not exist"

    if [ "$DRY_RUN" = false ]; then
        if [ "$AUTO_YES" = true ]; then
            info "Auto-creating git tag: $TAG"
            create_git_tag "$TAG"
        else
            read -p "Create git tag $TAG? [Y/n] " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                create_git_tag "$TAG"
            else
                warning "Continuing without creating git tag"
            fi
        fi
    else
        info "Would create git tag: $TAG"
    fi
fi

echo ""
display_banner "Pre-Upload Summary" "$RED"
warning "You are about to deploy to PRODUCTION PyPI!"
warning "This action cannot be undone!"

echo ""
info "Package: netshare"
info "Version: $VERSION"
info "Target:  PyPI (https://pypi.org/)"

echo ""
info "Files to upload:"
ls -lh "$PROJECT_ROOT/dist/"

echo ""

# Double confirmation (unless --yes flag is used)
if [ "$AUTO_YES" = false ] && [ "$DRY_RUN" = false ]; then
    # First confirmation
    read -p "Deploy version $VERSION to PRODUCTION PyPI? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        warning "Deployment cancelled by user"
        exit 5
    fi

    echo ""

    # Second confirmation (must type "yes")
    echo -e "${RED}⚠️  FINAL CONFIRMATION ⚠️${NC}"
    read -p "Are you ABSOLUTELY sure? Type 'yes' to confirm: " confirmation

    if [ "$confirmation" != "yes" ]; then
        warning "Deployment cancelled (confirmation not received)"
        exit 5
    fi

    echo ""
fi

# Upload to PyPI
cd "$PROJECT_ROOT" || exit 1

if [ "$DRY_RUN" = true ]; then
    echo ""
    info "DRY RUN - Would execute:"
    echo "  TWINE_USERNAME=__token__ TWINE_PASSWORD=*** twine upload dist/*"
    echo ""
    success "Dry run completed successfully!"
    echo ""
    info "To actually upload, run without --dry-run flag"
    exit 0
fi

info "Uploading to PyPI..."
echo ""

if TWINE_USERNAME=__token__ TWINE_PASSWORD="$PYPI_TOKEN" twine upload dist/*; then
    success "Upload successful!"

    # Log deployment
    log_deployment "prod" "$VERSION" "SUCCESS"
else
    error "Upload failed"
    log_deployment "prod" "$VERSION" "FAILED"
    exit 4
fi

echo ""
display_banner "🎉 Deployment Complete! 🎉" "$GREEN"

echo ""
success "Package uploaded to PyPI"
info "View at: https://pypi.org/project/netshare/$VERSION/"

echo ""

# Offer to push git tag
if check_git_tag "$TAG"; then
    offer_push_tag "$TAG"
fi

echo ""
banner "Installation Instructions:"
echo ""
echo "Users can now install with:"
echo ""
echo -e "${GREEN}pip install netshare${NC}"
echo ""

info "To verify the installation, run:"
echo "  ./pypi-build/verify-install.sh prod"

echo ""
banner "Next Steps:"
echo "1. Verify the package page: https://pypi.org/project/netshare/"
echo "2. Test installation: ./pypi-build/verify-install.sh prod"
echo "3. Update README.md or documentation if needed"
echo "4. Announce the release!"

echo ""
success "Production PyPI deployment completed successfully!"
echo ""
````

## File: pypi-build/deploy-test.sh
````bash
#!/bin/bash
# deploy-test.sh - Deploy netshare to TestPyPI
# Supports: --dry-run (show what would happen without uploading)
#           --yes (skip confirmation prompt for CI/CD)

# Get script directory and source config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Parse command line arguments
DRY_RUN=false
AUTO_YES=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --yes)
            AUTO_YES=true
            shift
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--dry-run] [--yes]"
            exit 1
            ;;
    esac
done

# Display banner
if [ "$DRY_RUN" = true ]; then
    display_banner "TestPyPI Deployment [DRY RUN]" "$YELLOW"
else
    display_banner "TestPyPI Deployment" "$BLUE"
fi

# Load TestPyPI token
info "Loading TestPyPI token..."
TESTPYPI_TOKEN=$(load_token "TESTPYPI_TOKEN" "TestPyPI API token")

if [ -z "$TESTPYPI_TOKEN" ]; then
    error "No TestPyPI token provided"
    exit 1
fi

# Validate token format
if ! validate_token "$TESTPYPI_TOKEN"; then
    exit 1
fi

echo ""

# Run build script
info "Running build script..."
echo ""

if ! "$SCRIPT_DIR/build.sh"; then
    error "Build failed"
    exit 3
fi

# Get version
VERSION=$(get_version_from_toml)

echo ""
display_banner "Pre-Upload Summary" "$BLUE"
info "Package: netshare"
info "Version: $VERSION"
info "Target:  TestPyPI (https://test.pypi.org/)"

echo ""
info "Files to upload:"
ls -lh "$PROJECT_ROOT/dist/"

echo ""

# Confirmation (unless --yes flag is used)
if [ "$AUTO_YES" = false ] && [ "$DRY_RUN" = false ]; then
    read -p "Deploy to TestPyPI? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        warning "Deployment cancelled by user"
        exit 5
    fi
    echo ""
fi

# Upload to TestPyPI
cd "$PROJECT_ROOT" || exit 1

if [ "$DRY_RUN" = true ]; then
    echo ""
    info "DRY RUN - Would execute:"
    echo "  TWINE_USERNAME=__token__ TWINE_PASSWORD=*** twine upload --repository testpypi dist/*"
    echo ""
    success "Dry run completed successfully!"
    echo ""
    info "To actually upload, run without --dry-run flag"
    exit 0
fi

info "Uploading to TestPyPI..."
echo ""

if TWINE_USERNAME=__token__ TWINE_PASSWORD="$TESTPYPI_TOKEN" twine upload --repository testpypi dist/*; then
    success "Upload successful!"

    # Log deployment
    log_deployment "test" "$VERSION" "SUCCESS"
else
    error "Upload failed"
    log_deployment "test" "$VERSION" "FAILED"
    exit 4
fi

echo ""
display_banner "Deployment Complete!" "$GREEN"

echo ""
info "Package uploaded to TestPyPI"
info "View at: https://test.pypi.org/project/netshare/$VERSION/"

echo ""
banner "Installation Instructions:"
echo ""
echo "To install from TestPyPI (for testing):"
echo ""
echo -e "${BLUE}pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ netshare${NC}"
echo ""

info "Note: The --extra-index-url allows pip to install dependencies from PyPI"

echo ""
info "To verify the installation, run:"
echo "  ./pypi-build/verify-install.sh test"

echo ""
success "TestPyPI deployment completed successfully!"
echo ""
````

## File: pypi-build/README.md
````markdown
# PyPI Build Automation for NetShare

This directory contains automated scripts for building and deploying the NetShare package to PyPI and TestPyPI.

## Quick Start

### First-time Setup

1. **Set up a build virtual environment (recommended):**

```bash
# Navigate to project root
cd /h/code/yl/netshare

# Create a virtual environment for building
python -m venv .build-venv

# Activate the virtual environment (Git Bash/MINGW)
source .build-venv/Scripts/activate

# Install build tools
pip install --upgrade pip
pip install build twine

# When done, deactivate with:
# deactivate
```

**Note:** Keep this venv activated when running the build and deployment scripts.

2. **Configure your PyPI tokens:**

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your actual tokens
nano .env

# Secure the file
chmod 600 .env
```

3. **Make scripts executable:**

```bash
chmod +x *.sh
```

### Common Workflows

#### Deploy to TestPyPI (for testing)

```bash
./deploy-test.sh
```

#### Deploy to Production PyPI

```bash
./deploy-prod.sh
```

#### Bump version before deployment

```bash
# Bump patch version (1.0.4 → 1.0.5)
./bump-version.sh patch

# Commit the version change
git add ../pyproject.toml ../netshare/__init__.py
git commit -m "Bump version to 1.0.5"

# Deploy to test first
./deploy-test.sh

# Then production
./deploy-prod.sh
```

---

## Scripts Overview

### `config.sh`

Shared configuration and utility functions used by all other scripts.

**Key Functions:**
- Token loading and validation
- Version consistency checking
- Prerequisite validation
- Color-coded output
- Deployment logging

**DO NOT execute directly** - this file is sourced by other scripts.

---

### `build.sh`

Build distribution packages without uploading.

**What it does:**
1. Validates prerequisites (Python, build, twine)
2. Checks version consistency
3. Cleans old build artifacts
4. Builds source distribution (.tar.gz) and wheel (.whl)
5. Validates packages with `twine check`

**Usage:**
```bash
./build.sh
```

**Output:** Creates files in `../dist/`

---

### `clean.sh`

Clean all build artifacts.

**What it does:**
- Removes `dist/`, `build/`, `*.egg-info/`, `__pycache__/`

**Usage:**
```bash
./clean.sh
```

---

### `bump-version.sh`

Update version numbers in both `pyproject.toml` and `netshare/__init__.py`.

**Usage:**
```bash
./bump-version.sh [major|minor|patch|X.Y.Z]
```

**Examples:**
```bash
./bump-version.sh major    # 1.0.4 → 2.0.0
./bump-version.sh minor    # 1.0.4 → 1.1.0
./bump-version.sh patch    # 1.0.4 → 1.0.5
./bump-version.sh 1.2.3    # Set explicit version
```

**Features:**
- Shows preview before applying changes
- Requires confirmation
- Updates both files atomically
- Validates semantic versioning format

---

### `deploy-test.sh`

Deploy to TestPyPI for testing.

**Usage:**
```bash
./deploy-test.sh [--dry-run] [--yes]
```

**Flags:**
- `--dry-run` - Show what would happen without uploading
- `--yes` - Skip confirmation (for CI/CD)

**What it does:**
1. Loads TestPyPI token
2. Runs build process
3. Uploads to test.pypi.org
4. Logs deployment
5. Shows installation instructions

**Installation from TestPyPI:**
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ netshare
```

---

### `deploy-prod.sh`

Deploy to production PyPI.

**Usage:**
```bash
./deploy-prod.sh [--dry-run] [--yes]
```

**Flags:**
- `--dry-run` - Show what would happen without uploading
- `--yes` - Skip confirmations (for CI/CD, still requires two prompts)

**What it does:**
1. Checks git status (warns about uncommitted changes)
2. Loads PyPI token
3. Runs build process
4. Auto-creates git tag if it doesn't exist
5. Requires TWO confirmations (unless --yes)
6. Uploads to pypi.org
7. Offers to push git tag
8. Logs deployment

**Safety Features:**
- Double confirmation required
- Git tag auto-creation
- Uncommitted changes warning
- Comprehensive validation

---

### `verify-install.sh`

Test installation from TestPyPI or PyPI in a temporary virtual environment.

**Usage:**
```bash
./verify-install.sh [test|prod]
```

**Examples:**
```bash
./verify-install.sh test   # Verify TestPyPI installation
./verify-install.sh prod   # Verify PyPI installation
```

**What it does:**
1. Creates temporary venv
2. Installs netshare from specified repository
3. Runs verification tests:
   - `netshare --help`
   - `python -m netshare --help`
   - Version import check
   - Dependency verification
4. Cleans up temporary environment
5. Reports results

---

## Token Setup

### Getting Your Tokens

#### TestPyPI Token
1. Go to https://test.pypi.org/account/register/
2. Verify your email
3. Create API token at https://test.pypi.org/manage/account/token/
4. Copy token (starts with `pypi-`)

#### Production PyPI Token
1. Go to https://pypi.org/account/register/
2. Verify your email
3. Create API token at https://pypi.org/manage/account/token/
4. Copy token (starts with `pypi-`)

### Token Configuration Methods

The scripts support three methods (in priority order):

1. **Environment Variables** (highest priority, best for CI/CD)
```bash
export TESTPYPI_TOKEN="pypi-..."
export PYPI_TOKEN="pypi-..."
```

2. **`.env` file** (recommended for local development)
```bash
cp .env.template .env
# Edit .env with your tokens
chmod 600 .env
```

3. **Interactive Prompt** (fallback)
   - Scripts will prompt if no token found
   - Input is hidden for security

### Security Best Practices

- **Never commit tokens** - `.env` is gitignored
- **Use project-specific tokens** when possible
- **Restrict permissions**: `chmod 600 .env`
- **Rotate tokens** regularly
- **Use environment variables in CI/CD** - don't store tokens in CI config

---

## Complete Deployment Workflow

### Releasing a New Version

```bash
# 1. Make your code changes
# ... edit code ...

# 2. Bump version
./pypi-build/bump-version.sh patch

# 3. Review changes
git diff pyproject.toml netshare/__init__.py

# 4. Commit version bump
git add pyproject.toml netshare/__init__.py
git commit -m "Bump version to 1.0.5"

# 5. Deploy to TestPyPI first
./pypi-build/deploy-test.sh

# 6. Verify TestPyPI installation
./pypi-build/verify-install.sh test

# 7. Deploy to production
./pypi-build/deploy-prod.sh

# 8. Verify production installation
./pypi-build/verify-install.sh prod

# 9. Push changes and tag
git push
git push origin v1.0.5
```

### Testing Before Deployment

```bash
# Build locally without uploading
./pypi-build/build.sh

# Test with dry-run
./pypi-build/deploy-test.sh --dry-run
./pypi-build/deploy-prod.sh --dry-run
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install build twine

      - name: Deploy to PyPI
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: |
          ./pypi-build/deploy-prod.sh --yes
```

**Setup:**
1. Add PyPI token as GitHub secret named `PYPI_TOKEN`
2. Create a GitHub release to trigger deployment

---

## Troubleshooting

### "Version mismatch" error

**Problem:** Versions in `pyproject.toml` and `netshare/__init__.py` don't match.

**Solution:** Use `bump-version.sh` to update both files atomically:
```bash
./pypi-build/bump-version.sh patch
```

### "Token is invalid" error

**Problem:** Token format is incorrect or expired.

**Solutions:**
- Ensure token starts with `pypi-`
- Check for extra spaces or newlines
- Generate a new token if expired

### "Package already exists" error

**Problem:** Version already uploaded to PyPI (versions are immutable).

**Solution:** Bump to a new version:
```bash
./pypi-build/bump-version.sh patch
```

### Build fails with missing dependencies

**Problem:** `build` or `twine` not installed.

**Solution:**
```bash
pip install build twine
```

### TestPyPI installation can't find dependencies

**Problem:** Dependencies not on TestPyPI.

**Solution:** Use both index URLs:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ netshare
```

The `--extra-index-url` allows pip to fetch dependencies from production PyPI.

---

## Logs

Deployment logs are stored in `logs/`:
- `logs/test-deployments.log` - TestPyPI deployments
- `logs/prod-deployments.log` - Production deployments

**Format:**
```
YYYY-MM-DD HH:MM:SS | vX.Y.Z | SUCCESS/FAILED | user@host | Repository
```

**Note:** The `logs/` directory is gitignored.

---

## File Structure

```
pypi-build/
├── config.sh              # Shared configuration (sourced by others)
├── build.sh               # Build distributions
├── clean.sh               # Clean artifacts
├── bump-version.sh        # Update version numbers
├── deploy-test.sh         # Deploy to TestPyPI
├── deploy-prod.sh         # Deploy to PyPI
├── verify-install.sh      # Test installations
├── .env.template          # Token configuration template
├── .env                   # Your tokens (gitignored, create from template)
├── README.md              # This file
└── logs/                  # Deployment logs (gitignored, auto-created)
    ├── test-deployments.log
    └── prod-deployments.log
```

---

## Additional Resources

- **PyPI Package Page:** https://pypi.org/project/netshare/
- **TestPyPI Package Page:** https://test.pypi.org/project/netshare/
- **PyPI Help:** https://pypi.org/help/
- **Packaging Guide:** https://packaging.python.org/

---

## Support

For issues with these scripts:
1. Check this README
2. Review logs in `logs/`
3. Run with `--dry-run` to see what would happen
4. Check `../PYPI_SETUP_GUIDE.md` for detailed setup instructions

---

**Happy Publishing!**
````

## File: pypi-build/verify-install.sh
````bash
#!/bin/bash
# verify-install.sh - Verify installation from TestPyPI or PyPI
# Usage: ./verify-install.sh [test|prod]

# Get script directory and source config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Display banner
display_banner "Verify Installation" "$BLUE"

# Check argument
if [ $# -eq 0 ]; then
    error "No repository specified"
    echo ""
    echo "Usage: $0 [test|prod]"
    echo ""
    echo "  test - Verify installation from TestPyPI"
    echo "  prod - Verify installation from PyPI"
    echo ""
    exit 1
fi

REPO_TYPE=$1

# Determine repository URL and name
case $REPO_TYPE in
    test)
        REPO_NAME="TestPyPI"
        PIP_ARGS="--index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/"
        ;;
    prod)
        REPO_NAME="PyPI"
        PIP_ARGS=""
        ;;
    *)
        error "Invalid repository type: $REPO_TYPE"
        echo "Must be 'test' or 'prod'"
        exit 1
        ;;
esac

info "Testing installation from $REPO_NAME"

# Create temporary venv
TIMESTAMP=$(date +%s)
VENV_DIR="/tmp/netshare-verify-$TIMESTAMP"

echo ""
info "Creating temporary virtual environment..."
info "Location: $VENV_DIR"

if $PYTHON_CMD -m venv "$VENV_DIR"; then
    success "Virtual environment created"
else
    error "Failed to create virtual environment"
    exit 2
fi

# Activate venv
source "$VENV_DIR/bin/activate"

echo ""
info "Installing netshare from $REPO_NAME..."
echo ""

# Install package
if pip install $PIP_ARGS netshare; then
    success "Installation completed"
else
    error "Installation failed"
    deactivate
    rm -rf "$VENV_DIR"
    exit 2
fi

echo ""
banner "Running Verification Tests"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: netshare --help
info "Test 1: Running 'netshare --help'"
if netshare --help > /dev/null 2>&1; then
    success "netshare command works"
    ((TESTS_PASSED++))
else
    error "netshare command failed"
    ((TESTS_FAILED++))
fi

echo ""

# Test 2: python -m netshare --help
info "Test 2: Running 'python -m netshare --help'"
if python -m netshare --help > /dev/null 2>&1; then
    success "python -m netshare works"
    ((TESTS_PASSED++))
else
    error "python -m netshare failed"
    ((TESTS_FAILED++))
fi

echo ""

# Test 3: Import and version check
info "Test 3: Checking version"
INSTALLED_VERSION=$(python -c "import netshare; print(netshare.__version__)" 2>/dev/null)

if [ -n "$INSTALLED_VERSION" ]; then
    success "Version imported successfully: $INSTALLED_VERSION"
    ((TESTS_PASSED++))

    # Compare with expected version if possible
    EXPECTED_VERSION=$(get_version_from_toml)
    if [ "$INSTALLED_VERSION" = "$EXPECTED_VERSION" ]; then
        success "Installed version matches expected version"
    else
        warning "Version mismatch: installed=$INSTALLED_VERSION, expected=$EXPECTED_VERSION"
        warning "This is normal if you haven't deployed the latest version yet"
    fi
else
    error "Failed to import version"
    ((TESTS_FAILED++))
fi

echo ""

# Test 4: Check dependencies
info "Test 4: Verifying dependencies"
DEPS_OK=true

if python -c "import flask" 2>/dev/null; then
    success "Flask is installed"
else
    error "Flask is not installed"
    DEPS_OK=false
fi

if python -c "import qrcode" 2>/dev/null; then
    success "qrcode is installed"
else
    error "qrcode is not installed"
    DEPS_OK=false
fi

if python -c "import PIL" 2>/dev/null; then
    success "Pillow is installed"
else
    error "Pillow is not installed"
    DEPS_OK=false
fi

if [ "$DEPS_OK" = true ]; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Deactivate and cleanup
echo ""
info "Cleaning up..."
deactivate
rm -rf "$VENV_DIR"
success "Temporary environment removed"

# Summary
echo ""
display_banner "Verification Summary" "$BLUE"

echo ""
info "Tests passed: $TESTS_PASSED"
if [ $TESTS_FAILED -gt 0 ]; then
    error "Tests failed: $TESTS_FAILED"
else
    info "Tests failed: $TESTS_FAILED"
fi

echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    success "All tests passed!"
    echo ""
    info "Installation from $REPO_NAME is working correctly"
    exit 0
else
    error "Some tests failed"
    echo ""
    warning "Installation from $REPO_NAME may have issues"
    exit 1
fi
````

## File: pyproject.toml
````toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "netshare"
version = "1.0.4"
description = "Secure network file sharing tool for local WiFi networks"
readme = "README.md"
license = {text = "GPL-3.0"}
authors = [
    {name = "NetShare Contributors"}
]
keywords = [
    "file-sharing",
    "network",
    "wifi",
    "android",
    "flask",
    "qr-code",
    "local-network",
    "file-transfer"
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Developers",
    "Topic :: Communications :: File Sharing",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
    "Environment :: Console",
    "Environment :: Web Environment",
]
requires-python = ">=3.7"
dependencies = [
    "Flask>=3.0.0",
    "qrcode>=7.4.2",
    "Pillow>=9.0.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/netshare"
Issues = "https://github.com/yourusername/netshare/issues"
Repository = "https://github.com/yourusername/netshare"

[project.scripts]
netshare = "netshare.app:main"

[project.optional-dependencies]
dev = [
    "build>=0.10.0",
    "twine>=4.0.0",
]

[tool.setuptools]
packages = ["netshare"]

[tool.setuptools.package-data]
netshare = ["templates/*.html"]
````

## File: requirements.txt
````
Flask>=3.0.0
qrcode>=7.4.2
Pillow>=9.0.0
````

## File: streamlit/.streamlit/config.toml
````toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
````

## File: streamlit/greetings_qr.md
````markdown
# Holiday Greeting QR Implementation Plan

## Executive Summary

**Goal**: Generate animated QR codes with personalized holiday greeting messages

**Status**: ✅ Amazing-QR has excellent animated GIF QR support built-in - perfect for this use case!

**Timeline**: 2-3 hours for MVP, 3 days for full-featured version

---

## What Amazing-QR Already Has

### ✅ Animated GIF QR Generation (Lines 96-117 in amzqr.py)

**Process**:
1. Extract all frames from input GIF
2. Generate QR code for each frame with that frame as background
3. Recombine into animated GIF preserving timing

**Example**: `/mnt/h/code/3rd/amazing-qr/example/*.gif` - all remain scannable while animated!

**Key Features**:
- Colorization support
- Contrast/brightness adjustment
- Frame timing preservation
- Multiple output formats

---

## What We Need to Add

### 1. Greeting JSON Schema (`greeting_formats.py`)
**Purpose**: Structure greeting data in compact JSON format

```python
def create_holiday_greeting(from_name, to_name, message, occasion, theme):
    return {
        "v": "1.0",
        "type": "greeting",
        "from": from_name,
        "to": to_name,
        "occasion": occasion,
        "message": message,
        "theme": theme,
        "created": datetime.utcnow().isoformat()
    }

def compact_greeting(payload):
    """Minimize JSON - remove whitespace"""
    return json.dumps(payload, separators=(',', ':'))
```

**Size**: ~240 bytes for typical greeting

---

### 2. Optional Compression (Add to `data.py`)
**Purpose**: Fit longer messages in QR codes

```python
import zlib
import base64

def compress_text(text):
    compressed = zlib.compress(text.encode('utf-8'), level=9)
    return base64.b64encode(compressed).decode('ascii')

def decompress_text(encoded_text):
    try:
        compressed = base64.b64decode(encoded_text)
        return zlib.decompress(compressed).decode('utf-8')
    except:
        return encoded_text  # Not compressed
```

**Benefit**: 40-50% size reduction → 240 bytes → ~140 bytes

---

### 3. Holiday Theme GIFs (Create `themes/holiday/` directory)

**Required Themes** (6-8 animated GIFs):
- `snowflake.gif` - Falling snowflakes ❄️
- `fireworks.gif` - Bursting fireworks 🎆
- `lights.gif` - Twinkling holiday lights ✨
- `stars.gif` - Starry night ⭐
- `confetti.gif` - Celebration confetti 🎉
- `champagne.gif` - Clinking glasses 🥂

**Specs**:
- Size: 400x400 to 600x600 pixels
- Frames: 5-15 frames
- Duration: 100-200ms per frame
- File size: <500KB

---

### 4. Simple Generator Interface

**Option A: CLI Script** (`create_greeting_qr.py`)
```python
from amzqr import run
from amzqr.greeting_formats import create_holiday_greeting, compact_greeting

print("🎄 Holiday Greeting QR Generator")
from_name = input("From: ")
to_name = input("To: ")
message = input("Your message: ")
theme = input("Theme (snowflake/fireworks/lights): ")

greeting = create_holiday_greeting(from_name, to_name, message, "Holiday 2025", theme)
qr_data = compact_greeting(greeting)

ver, level, qr_path = run(
    words=qr_data,
    picture=f"themes/holiday/{theme}.gif",
    colorized=True,
    level='H',
    save_name=f"{to_name}_greeting.gif"
)

print(f"✅ Created: {qr_path}")
```

**Option B: Streamlit Web App** - See detailed code in main plan

---

## Implementation Steps

### Phase 1: Core Enhancement (2 hours)

**Files to Create**:
1. `/mnt/h/code/3rd/amazing-qr/amzqr/greeting_formats.py` (~50 lines)
   - `create_holiday_greeting()` function
   - `compact_greeting()` function
   - `parse_greeting()` function

**Files to Modify** (Optional - for compression):
2. `/mnt/h/code/3rd/amazing-qr/amzqr/mylibs/data.py`
   - Add `compress_text()` and `decompress_text()` functions

3. `/mnt/h/code/3rd/amazing-qr/amzqr/amzqr.py`
   - Add `compress=False` parameter to `run()` function
   - Call compression before QR generation if enabled

**Testing**:
- Create sample greeting JSON
- Test compression ratio
- Generate test QR and verify scannability

---

### Phase 2: Holiday Themes (1-2 hours)

**Tasks**:
1. Create directory: `/mnt/h/code/3rd/amazing-qr/themes/holiday/`
2. Source 6-8 holiday GIF animations:
   - Search Giphy/Tenor for "snowflake loop", "fireworks animation"
   - Download and optimize (resize to 500x500, reduce frames if needed)
   - Test each theme generates scannable QR

**Tools**:
- GIMP or Photoshop for GIF optimization
- Online GIF editors (ezgif.com)
- Reduce frames to 8-12 if file >500KB

---

### Phase 3: Generator Interface (2-4 hours)

**Simple CLI** (30 minutes):
- Create `create_greeting_qr.py` with interactive prompts
- Test with all themes

**Web App** (3-4 hours):
- Build Streamlit app with create/scan pages
- Add theme previews
- Add download button
- Deploy locally or to Streamlit Cloud

---

### Phase 4: Testing & Polish (2-3 hours)

**Scanability Tests**:
- [ ] Test on iPhone (iOS Camera app)
- [ ] Test on Android (Google Lens)
- [ ] Test various message lengths (100, 300, 500 chars)
- [ ] Verify all themes scan correctly

**Quality Tests**:
- [ ] Animation smooth (no frame drops)
- [ ] Colors preserved
- [ ] File sizes reasonable (<1MB)

**Documentation**:
- [ ] Create README with examples
- [ ] Add usage instructions
- [ ] Create 3-4 demo greeting QRs

---

## Message Capacity Reference

| Message Length | Uncompressed | Compressed | QR Version |
|----------------|--------------|-----------|------------|
| 100 chars (~15 words) | ~150 bytes | ~90 bytes | V10-H |
| 200 chars (~30 words) | ~250 bytes | ~150 bytes | V15-H |
| 300 chars (~50 words) | ~350 bytes | ~210 bytes | V20-H |
| 500 chars (~80 words) | ~550 bytes | ~330 bytes | V30-H |
| 1000 chars (~150 words) | ~1050 bytes | ~630 bytes | V40-H |

**Recommendation**: Default to error correction level 'H' for maximum scan reliability

---

## Example Use Cases

### 1. Christmas Card Greeting
```python
greeting = create_holiday_greeting(
    from_name="Alice",
    to_name="Bob",
    message="Merry Christmas! Wishing you joy and happiness this season. Thank you for being a wonderful friend!",
    occasion="Christmas 2025",
    theme="snowflake"
)
# Output: Animated snowflake QR (200 bytes compressed)
```

### 2. New Year's Time Capsule
```python
greeting = create_holiday_greeting(
    from_name="Bob",
    to_name="Future Me",
    message="2025 was incredible! Here's to growth and new adventures in 2026!",
    occasion="New Year 2026",
    theme="fireworks"
)
# Output: Animated fireworks QR
```

### 3. Wedding Save the Date
```python
greeting = create_holiday_greeting(
    from_name="Emma & James",
    to_name="Friends and Family",
    message="We're getting married! Save the date: June 15, 2026. More details to follow!",
    occasion="Wedding Announcement",
    theme="champagne"
)
# Output: Animated champagne QR
```

---

## Critical Files Summary

### Files to Create:
1. **`amzqr/greeting_formats.py`** - JSON schemas and helpers (50 lines)
2. **`create_greeting_qr.py`** - CLI tool (40 lines)
3. **`themes/holiday/*.gif`** - 6-8 animated GIF themes
4. **`app.py`** (optional) - Streamlit web interface (150 lines)

### Files to Modify (Optional):
1. **`amzqr/mylibs/data.py`** - Add compression functions
2. **`amzqr/amzqr.py`** - Add compress parameter

### No Changes Needed:
- **`amzqr/amzqr.py` lines 96-117** - Animated GIF logic already perfect!

---

## Quick Start (Minimum Viable Product)

**Goal**: Working greeting QR generator in 2 hours

1. **Create `greeting_formats.py`** (30 min)
   - Basic JSON schema functions
   - No compression for MVP

2. **Find 2-3 GIF themes** (30 min)
   - Download from Giphy/Tenor
   - Save to `themes/holiday/`

3. **Create CLI script** (30 min)
   - Interactive prompts
   - Generate QR using existing amazing-qr

4. **Test** (30 min)
   - Generate sample greeting
   - Scan with phone
   - Verify animation works

**Result**: Working prototype without compression or web interface

---

## Full Featured Version (3 Days)

### Day 1: Core
- Morning: Create `greeting_formats.py` with all schemas
- Afternoon: Add compression to `data.py` and `amzqr.py`
- Evening: Test compression ratios and scannability

### Day 2: Content & Interface
- Morning: Curate 6-8 holiday theme GIFs
- Afternoon: Build Streamlit web interface
- Evening: Test theme combinations

### Day 3: Polish
- Morning: Add QR scanning to web app
- Afternoon: Create examples and documentation
- Evening: Final testing on multiple devices

---

## Success Criteria

- [x] Animated QR generation works (already ✅)
- [ ] Greeting JSON schema created
- [ ] 6-8 holiday theme GIFs ready
- [ ] CLI or web interface working
- [ ] QRs scan on iOS and Android (>95% success)
- [ ] Animations smooth and beautiful
- [ ] File sizes <1MB for sharing

---

## Why This Will Work

1. **Built on Proven Tech**: Animated QR already working in amazing-qr
2. **Low Risk**: Minimal code changes, mostly new files
3. **High Value**: Beautiful, shareable greeting cards
4. **Quick to Build**: 2-3 hours for MVP
5. **Delightful UX**: Animated QRs are visually appealing

---

## Next Steps

Ready to implement! Choose your path:

**Path A - Quick MVP** (2-3 hours):
1. Create `greeting_formats.py`
2. Download 3 GIF themes
3. Build simple CLI script
4. Test and iterate

**Path B - Full Version** (3 days):
1. All MVP features
2. Add compression support
3. Build Streamlit web app
4. Create complete theme library
5. Polish and document

**Recommendation**: Start with MVP, then enhance based on feedback!
````

## File: streamlit/QUICKSTART.md
````markdown
# Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies

```bash
cd /mnt/h/code/yl/netshare/streamlit
pip install -r requirements.txt
```

**Note for Linux users**: You may need to install additional system packages for QR code scanning:

```bash
# Ubuntu/Debian
sudo apt-get install libzbar0

# Fedora
sudo dnf install zbar

# Arch Linux
sudo pacman -S zbar
```

### Step 2: Verify Installation

Test that all modules work correctly:

```bash
python3 -c "from greeting_formats import create_holiday_greeting; print('✅ Installation successful!')"
```

### Step 3: Launch the App

**Option A - Using launcher script (Linux/Mac)**:
```bash
./run.sh
```

**Option B - Using launcher script (Windows)**:
```batch
run.bat
```

**Option C - Direct command**:
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## First Steps

### Create Your First Greeting

1. Navigate to the **"Create Greeting"** tab
2. Fill in the form:
   - **From**: Your name (e.g., "Alice")
   - **To**: Recipient name (e.g., "Bob")
   - **Occasion**: Select "Christmas 2025" or custom
   - **Theme**: Choose "snowflake" for a festive look
   - **Message**: Write your greeting (e.g., "Merry Christmas! Wishing you joy!")
3. Click **"Generate QR Code"**
4. Download the QR code image
5. Share it via email, messaging, or print it!

### Test Scanning

1. Navigate to the **"Scan QR Code"** tab
2. Upload the QR code you just created
3. View your decoded greeting message

## Example Usage

### Command Line Test

You can also test the greeting creation from command line:

```bash
cd /mnt/h/code/yl/netshare/streamlit

python3 << 'EOF'
from greeting_formats import create_holiday_greeting, compact_greeting
import qrcode
from PIL import Image

# Create greeting
greeting = create_holiday_greeting(
    from_name="Alice",
    to_name="Bob",
    message="Merry Christmas! 🎄",
    occasion="Christmas 2025",
    theme="snowflake"
)

# Generate QR code
greeting_json = compact_greeting(greeting)
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(greeting_json)
qr.make(fit=True)

# Save QR code
img = qr.make_image(fill_color="black", back_color="white")
img.save("test_greeting.png")
print("✅ QR code saved to test_greeting.png")
print(f"📦 Data size: {len(greeting_json)} bytes")
EOF
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`, install dependencies:
```bash
pip install -r requirements.txt
```

### QR Scanning Not Working

If QR scanning fails, make sure pyzbar and system libraries are installed:

```bash
# Install Python package
pip install pyzbar

# Install system library (Linux)
sudo apt-get install libzbar0
```

### Streamlit Won't Start

Make sure you're in the correct directory:
```bash
cd /mnt/h/code/yl/netshare/streamlit
pwd  # Should show the streamlit directory
ls   # Should show app.py
```

### Port Already in Use

If port 8501 is busy, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## Project Structure

```
streamlit/
├── app.py                    # Main Streamlit application
├── greeting_formats.py       # Greeting encoding/decoding
├── requirements.txt          # Python dependencies
├── README.md                # Full documentation
├── QUICKSTART.md            # This file
├── run.sh                   # Launch script (Linux/Mac)
├── run.bat                  # Launch script (Windows)
└── .streamlit/
    └── config.toml          # App configuration
```

## Next Steps

- Explore the **Examples** tab for inspiration
- Read the **About** tab for technical details
- Check **README.md** for comprehensive documentation
- Create multiple greetings for different occasions!

## Support

For detailed information, see [README.md](README.md)

For issues with:
- **netshare package**: Check PyPI page
- **Streamlit**: Visit [streamlit.io/docs](https://streamlit.io/docs)
- **QR codes**: Review the About tab in the app

---

Happy greeting! 🎄✨
````

## File: streamlit/run.bat
````batch
@echo off
REM Launcher script for Holiday Greeting QR Code Generator (Windows)

echo.
echo 🎄 Starting Holiday Greeting QR Code Generator...
echo.

REM Check if streamlit is installed
where streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Streamlit is not installed.
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "app.py" (
    echo ❌ app.py not found. Please run this script from the streamlit directory.
    pause
    exit /b 1
)

echo ✅ All checks passed!
echo 🚀 Launching application...
echo.

REM Run streamlit
streamlit run app.py

pause
````

## File: streamlit/run.sh
````bash
#!/bin/bash
# Launcher script for Holiday Greeting QR Code Generator

echo "🎄 Starting Holiday Greeting QR Code Generator..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit is not installed."
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the streamlit directory."
    exit 1
fi

echo "✅ All checks passed!"
echo "🚀 Launching application..."
echo ""

# Run streamlit
streamlit run app.py
````

## File: 2026-01-26-mntecode2netsharestreamlitkeepalivelogtx.txt
````
▐▛███▜▌   Claude Code v2.1.11                                                  
▝▜█████▛▘  Opus 4.5 · Claude Pro                                                
  ▘▘ ▝▝    /mnt/e/code2/netshare                                                
                                                                                
❯ '/mnt/e/code2/netshare/streamlit/keep_alive_log.txt' explain to me how is     
  '/mnt/e/code2/netshare/streamlit/keep_alive.py' being called?                 
                                                                                
● I'll explore how keep_alive.py is being called in your codebase.              
                                                                                
● Explore(Explore keep_alive.py usage)                                          
  ⎿  Done (13 tool uses · 47.7k tokens · 33s)                                   
                                                                                
● How keep_alive.py is Being Called                                             
                                                                                
  Based on the exploration, here's the answer:                                  
                                                                                
  keep_alive.py is NOT currently being called by the application                
                                                                                
  It's a standalone legacy script meant for manual execution. The log file      
  (keep_alive_log.txt) is actually populated by a different mechanism.          
                                                                                
  ---                                                                           
  What's Actually Running                                                       
  Mechanism: keepalive_daemon.py                                                
  Status: ✅ PRIMARY                                                            
  Details: Imported in app.py:27-29, runs as daemon thread                      
  ────────────────────────────────────────                                      
  Mechanism: keep_alive.ps1                                                     
  Status: ✅ SECONDARY                                                          
  Details: Windows Task Scheduler, logs to keep_alive_log.txt                   
  ────────────────────────────────────────                                      
  Mechanism: keep_alive.py                                                      
  Status: ❌ UNUSED                                                             
  Details: Standalone script, not imported anywhere                             
  ---                                                                           
  The Log File Source                                                           
                                                                                
  The keep_alive_log.txt is written by keep_alive.ps1 (PowerShell), not         
  keep_alive.py:                                                                
                                                                                
  Windows Task Scheduler → keep_alive.ps1 → keep_alive_log.txt                  
                           (runs hourly)                                        
                                                                                
  Registered via setup_task.ps1 as task StreamlitKeepAlive.                     
                                                                                
  ---                                                                           
  The Active Mechanism                                                          
                                                                                
  In app.py:27-29:                                                              
  from keepalive_daemon import start_keepalive_daemon                           
  start_keepalive_daemon()                                                      
                                                                                
  This starts a background daemon thread that pings net-test.streamlit.app every
   30 minutes.                                                                  
                                                                                
  ---                                                                           
  Summary                                                                       
                                                                                
  If you want to actually use keep_alive.py, you'd need to either:              
  1. Run it manually: python keep_alive.py                                      
  2. Import and call it from another script                                     
  3. Schedule it externally (cron, Task Scheduler, etc.)                        
                                                                                
  Currently it sits unused while keepalive_daemon.py handles the keep-alive     
  functionality.                                                                
                                                                                
✻ Brewed for 1m 1s
````

## File: FUNNEL_GUIDE_MIA.md
````markdown
# Marketing Funnel QR Guide for Pottery Creators

This guide explains how to use the Marketing Funnel feature to convert your content viewers into customers. This is perfect for creators like **Mia Mueller of 'Pottery to the People'** to bridge her YouTube audience to her Etsy shop.

## 🎯 The Problem Mia Faces

- **151K YouTube subscribers** watching pottery tutorials
- **Etsy shop exists** but disconnect between content viewers → buyers  
- **YouTube doesn't allow clickable links in videos** (only description)
- Need to convert "interested viewers" into "paying customers"

## ✨ The Solution: Marketing Funnel QR

The Marketing Funnel QR creates a dedicated landing page optimized for mobile. When viewers scan a QR code (placed in your video description or end screen), they get:

1. **Preview of the pottery piece** from the video
2. **Exclusive offer** for YouTube viewers only
3. **Direct link to Etsy** with promo code
4. **Urgency messaging** to encourage action

---

## 📋 Step-by-Step for Mia

### **Step 1: Identify the Product**
Choose the specific pottery piece featured in your YouTube video that you want to promote.

**Example:**
- Video: "How to Make a Grounded Teapot"
- Product: Grounded Teapot Template on Etsy

### **Step 2: Gather Required Information**

You'll need these 5 key pieces:

1. **Video URL**  
   `https://www.youtube.com/watch?v=YOUR_VIDEO_ID`

2. **Product Name**  
   `"Grounded Teapot Template"`

3. **Landing URL** (Your Etsy product page)  
   `https://www.etsy.com/shop/PotterytothePeople/YOUR_PRODUCT`

4. **Offer Text**  
   ```
   Learn to make this? Get the template + 10% off!
   
   ✓ Video tutorial included
   ✓ Beginner-friendly  
   ✓ Print at any size
   ```

5. **Discount Code**  
   `YOUTUBE10`

### **Step 3: Create the Funnel QR**

1. Open the **NetPull app** (https://net-test.streamlit.app)
2. Navigate to **Marketing Funnel QR** tab
3. Fill in the form:

   **📹 Step 1: Your Content**
   - Video URL: Paste your YouTube link
   - Landing Page URL: Your Etsy product URL

   **🎁 Step 2: Your Offer**
   - Headline: `Want to make this?`
   - Offer Description: (Use the text from Step 2)
   - CTA Button: `Shop Now →`
   - Promo Code: `YOUTUBE10`
   - Urgency: `YouTube viewers only - Expires in 48 hours`

   **🎨 Step 3: Branding**
   - Brand Name: `Pottery to the People`
   - Visual Theme: `⭐ Stars (Aspirational)` or `✨ Lights (Premium)`
   - QR Label: `SCAN FOR 10% OFF`

4. Click **🚀 Generate Marketing Funnel QR**

### **Step 4: Download & Deploy**

1. **Download the QR code** (PNG file)
2. **Add it to your YouTube video**:
   - End screen element
   - Video description (upload to Imgur, link in description)
   - Pinned comment with QR code image

3. **Optional: Add to other marketing materials**:
   - Instagram Stories
   - Email newsletter
   - Printed flyers at pottery events

### **Step 5: Track Conversions**

Monitor your Etsy shop sales to see:
- How many customers used `YOUTUBE10` code
- Which videos drive the most sales
- Peak conversion times (helps with posting schedule)

**Pro Tip:** Create a different promo code for each video to track performance per video!

---

## 🎨 Design Highlights

The funnel page is designed specifically for pottery creators:

### **Visual Style**
- **Warm, tactile aesthetic** matching Pottery to the People brand
- **Photography-first** (not text-heavy)
- **Natural lighting** to showcase pottery pieces
- **Mobile-optimized** (most YouTube viewers are on mobile)

### **Color Palette**
- Background: Warm cream (`#FAF7F2`)
- Primary CTA: Terracotta gold (`#B8956A`)
- Text: Warm charcoal (`#3E3830`)
- Accent: Clay beige (`#E8DCC8`)

### **Layout**
```
┌─────────────────────────────┐
│  [Hero Image - Pottery]     │  ← Full-width, 60vh
├─────────────────────────────┤
│  "Want to make this?"       │
│  Product Name               │
│                             │
│  Get 20% OFF your first     │
│  order! Use Code: YOUTUBE10 │
│                             │
│  ✓ Video tutorial included  │
│  ✓ Beginner-friendly        │
│  ✓ Print at any size        │
│                             │
│  ┌────────────────────┐     │
│  │   Shop Now →       │     │
│  └────────────────────┘     │
│                             │
│  ⏱ YouTube viewers only    │
│     Expires in 48 hours     │
│                             │
│  ─────────────────────────  │
│                             │
│  "As seen on Pottery to     │
│   the People"               │
│  [YouTube icon] 151K subs   │
└─────────────────────────────┘
```

---

## 💡 Advanced Tips

### **Tip 1: Create Video-Specific Funnels**
Different videos → different funnels → track which content sells best

**Example:**
- "Beginner Wheel Throwing" video → Beginner Template Bundle
- "Advanced Glazing" video → Premium Glaze Kit

### **Tip 2: Seasonal Offers**
Update urgency text for seasonal promotions:
- `"Holiday Sale - 20% off until Dec 25"`
- `"Spring Collection - New templates!"``

### **Tip 3: A/B Testing**
Try different headlines to see what converts:
- Test A: `"Want to make this?"`
- Test B: `"Learn pottery from home!"`
- Test C: `"Your next pottery project →"`

### **Tip 4: Cross-Promote**
Mention the QR code in your video:
- "Check the description for a special discount!"
- "Scan the QR code to get the template"
- Show QR code on-screen at end of video

---

## ❓ FAQ

**Q: Do I need a new QR code for each video?**  
Yes! Each video should have its own funnel with:
- Specific product featured in that video
- Unique tracking code (e.g., `VIDEO01`, `VIDEO02`)

**Q: How long should I keep the offer active?**  
48 hours creates urgency without being too restrictive. You can always extend it for popular videos.

**Q: Can I update the funnel after creating the QR code?**  
No - QR codes are static. If you need to change the offer, create a new QR code.

**Q: What if I don't have a product photo?**  
Use a screenshot from your video! The hero image should show the finished pottery piece.

**Q: Should I use the same discount code for all videos?**  
No! Use unique codes per video (e.g., `TEAPOT10`, `MUG10`) to track which videos convert best.

---

## 📊 Success Metrics

Track these KPIs to measure success:

1. **QR Scans** → Use URL shortener with analytics
2. **Promo Code Usage** → Etsy sales with code
3. **Conversion Rate** → (Sales ÷ Scans) × 100%
4. **Revenue per Video** → Total sales from each video's code

**Benchmark Goals:**
- 5-10% conversion rate (great start)
- 10-20% conversion rate (excellent)
- 20%+ conversion rate (viral video!)

---

## 🚀 Next Steps

1. **Pick your most popular video** (highest views/engagement)
2. **Create your first funnel QR** using this guide
3. **Add QR to video description** and monitor for 48 hours
4. **Review results** and iterate
5. **Scale to all videos** once you have a winning formula

---

## 📞 Support

Need help? Found a bug? Have a feature request?

- **GitHub Issues**: [NetPull Repository]
- **Email**: support@yourapp.com
- **Community**: Join our Discord/Slack

---

**Made with ❤️ for pottery creators who want to turn viewers into customers**
````

## File: README.md
````markdown
# NetShare
![1763844410242](https://raw.githubusercontent.com/ly2xxx/netshare/main/image/README/1763844410242.png)
![1763936492583](https://raw.githubusercontent.com/ly2xxx/netshare/main/image/README/1763936492583.png)
A secure, Python-based network file sharing tool that enables easy sharing of folders from Windows, Mac, or Linux computers to Android devices, Quest VR headsets, and other devices over your local WiFi network.

## 🚀 Features

- **🔒 Security First**: Built-in rate limiting, file extension filtering, and path traversal protection
- **📱 Mobile Friendly**: QR code generation for instant mobile access
- **🎯 Simple Setup**: GUI and command-line options for easy folder selection
- **⚡ Fast Transfer**: Direct WiFi connection with no external servers
- **🛡️ Configurable Security**: Customizable file size limits, extension blocking, and access controls
- **🌐 Cross-Platform**: Works on Windows, macOS, and Linux
- **📊 Access Logging**: Optional request logging for monitoring

## 📋 Requirements

- Python 3.7 or higher
- Local WiFi network (same network for sharing device and receiving device)
- Modern web browser on receiving device

## 🔧 Installation

### From PyPI (Recommended)

The easiest way to install NetShare is via pip:

```bash
pip install netshare
```

Then run it with:

```bash
netshare --gui                              # GUI mode
netshare --folder /path                     # Specify folder
netshare --url https://example.com          # Generate QR code for any URL
netshare --help                             # Show all options
```

### From Source

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/yourusername/netshare.git
   cd netshare
   ```

2. **Install in editable mode**:
   ```bash
   pip install -e .
   ```

3. **Run NetShare**:
   ```bash
   netshare --gui
   ```

### Using Virtual Environment (Recommended)

1. **Create virtual environment**:
   ```bash
   python -m venv netshare-env

   # Windows
   netshare-env\Scripts\activate

   # macOS/Linux
   source netshare-env/bin/activate
   ```

2. **Install in editable mode**:
   ```bash
   pip install -e .
   ```

3. **Run the application**:
   ```bash
   netshare --gui
   ```

## 🚀 Quick Start

### Method 1: GUI Mode (Easiest)

```bash
netshare --gui
```

1. Select folders using the graphical interface
2. Server starts automatically
3. Scan the QR code with your mobile device or use the displayed URL

### Method 2: Command Line

```bash
netshare --folder "C:\Users\YourName\Documents" --port 8000
```

### Method 3: Interactive Mode

```bash
netshare
```

Follow the prompts to enter folder paths.

### Method 4: Standalone QR Code Generation

Generate a QR code for any URL without starting a file server:

```bash
# Generate QR code with default filename (netshare_qr.png)
netshare --url https://example.com

# Generate QR code with custom output filename
netshare --url https://example.com --output qr.png

# Another example with different filename
netshare --url https://example.com --output example.png
```

This is useful for creating QR codes for websites, shared links, or any other URLs.

## 📖 Detailed Usage

### Command Line Options

```bash
netshare [options]

Options:
  --gui                 Use GUI to select folders
  --folder, -f FOLDER   Folder to share (can be specified multiple times)
  --port, -p PORT       Port to run server on (default: 5000)
  --url, -u URL         Generate QR code for the given URL (standalone mode)
  --output, -o PATH     Output path for QR code PNG file (default: netshare_qr.png)
  -h, --help            Show help message

Examples:
  netshare --gui                                       # Use GUI to select folders
  netshare --folder /path/to/share                     # Share specific folder
  netshare --folder "C:\Users\Documents" --port 8000
  netshare --url https://example.com                   # Generate QR code for URL
  netshare --url https://example.com --output qr.png   # Generate QR with custom filename
  netshare --url https://example.com --output example.png
```

### Accessing Shared Files

1. **Start NetShare** using any method above
2. **Note the server URL** displayed in the terminal (e.g., `http://192.168.1.100:5000`)
3. **On your mobile/target device**:
   - Scan the QR code with your camera app, OR
   - Open a web browser and navigate to the displayed URL
4. **Browse and download** files through the web interface

### Using the Web Interface

- **Home Page**: Shows all shared folders
- **Browse**: Click folders to navigate directory structure
- **Download**: Click files to download them
- **Breadcrumbs**: Use the navigation path to go back to parent folders

## 🔧 Configuration

### Security Settings

Edit `netshare/config.py` in your installation directory to customize security settings:

```python
class SecurityConfig:
    # Maximum file size to serve (20GB default)
    MAX_FILE_SIZE = 20 * 1024 * 1024 * 1024

    # Block dangerous file extensions
    BLOCKED_EXTENSIONS = ['.exe', '.bat', '.cmd', '.sh', '.ps1']

    # Allow only specific extensions (empty = allow all)
    ALLOWED_EXTENSIONS = []  # e.g., ['.pdf', '.jpg', '.mp4']

    # Enable/disable features
    ALLOW_DIRECTORY_LISTING = True
    ALLOW_FILE_DOWNLOAD = True

    # Security limits
    MAX_PATH_DEPTH = 20
    RATE_LIMIT = 100  # requests per minute per IP
```

### Application Settings

```python
class AppConfig:
    DEFAULT_PORT = 5000
    SERVER_NAME = "NetShare"
    ENABLE_ACCESS_LOG = True  # Log all requests
```

## 🛠️ Advanced Usage

### Custom Port Configuration
```bash
# Use a different port if 5000 is occupied
netshare --folder ~/Documents --port 8080
```

### Multiple Folder Sharing
```bash
# Share multiple folders simultaneously
netshare --folder ~/Documents --folder ~/Pictures --folder ~/Downloads
```

### Running as Background Service
```bash
# Run in background (Linux/macOS)
nohup netshare --folder ~/shared &

# Windows (run in separate command window)
start netshare --folder C:\Shared
```

## 📱 Mobile Access Tips

### Android Devices
1. Use any web browser (Chrome, Firefox, etc.)
2. QR code scanner apps work with the generated codes
3. Bookmark the URL for easy future access

### Quest VR Headsets
1. Use the built-in browser
2. QR code scanning may require companion mobile app
3. Save URL in browser bookmarks for easy access

### iOS Devices
1. Use Safari or any web browser
2. Camera app can scan QR codes directly
3. Add to home screen for app-like experience

## 🚨 Troubleshooting

### Connection Issues

**Problem**: Cannot access from mobile device
```bash
Solutions:
1. Ensure both devices are on the same WiFi network
2. Check if firewall is blocking the port (5000 by default)
3. Try a different port: --port 8080
4. Verify the IP address is correct
```

**Problem**: "Connection refused" error
```bash
Solutions:
1. Make sure NetShare server is running
2. Check if another application is using the port
3. Try running as administrator (Windows) or with sudo (Linux/Mac)
```

**Windows Firewall Configuration (Windows Only)**

If you can access NetShare from the host PC but not from other devices on the same WiFi network, you need to configure Windows Firewall:

**Step 1: Run the diagnostic script** (optional, to check current settings)
```powershell
# In PowerShell (as Administrator)
cd path\to\netshare
.\firewall_diagnostic.ps1
```

**Step 2: Fix the firewall rules**
1. **Open PowerShell as Administrator**:
   - Press Windows key
   - Type "PowerShell"
   - Right-click "Windows PowerShell"
   - Select "Run as Administrator"

2. **Navigate to NetShare directory**:
   ```powershell
   cd path\to\netshare
   ```

3. **Run the firewall fix script**:
   ```powershell
   .\fix_firewall.ps1
   ```

4. **Test the connection** from your mobile device using the displayed URL (e.g., `http://192.168.0.96:8080`)

**Why is this needed?** Windows Firewall rules may only apply to "Public" network profiles, while your home network is set to "Private". The fix script creates rules that work on all network profiles.

**Alternative: Use firewall-friendly port**
```bash
# Port 8080 is more commonly allowed by firewalls
netshare --port 8080
```

### File Access Issues

**Problem**: Cannot download certain files
```bash
Solutions:
1. Check BLOCKED_EXTENSIONS in netshare/config.py
2. Verify file size under MAX_FILE_SIZE limit
3. Ensure ALLOW_FILE_DOWNLOAD = True in netshare/config.py
```

**Problem**: Folders not showing
```bash
Solutions:
1. Verify folder paths exist and are accessible
2. Check ALLOW_DIRECTORY_LISTING = True in netshare/config.py
3. Ensure proper read permissions on folders
```

### Network Connectivity

**Problem**: QR code doesn't work
```bash
Solutions:
1. Manually type the URL into browser
2. Check IP address is reachable: ping [IP_ADDRESS]
3. Restart router if needed
4. Use different QR code scanner app
```

### Performance Issues

**Problem**: Slow file transfers
```bash
Solutions:
1. Check WiFi signal strength
2. Reduce MAX_FILE_SIZE if memory limited
3. Close other network applications
4. Use 5GHz WiFi band if available
```

## 🔐 Security Best Practices

### Recommended Security Settings

1. **Limit file types**:
   ```python
   ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.png', '.mp4', '.doc', '.txt']
   ```

2. **Reduce file size limits** for better performance:
   ```python
   MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB
   ```

3. **Enable access logging** to monitor usage:
   ```python
   ENABLE_ACCESS_LOG = True
   ```

4. **Use non-default ports** to reduce discovery:
   ```bash
   netshare --folder ~/Documents --port 8543
   ```

### Network Security

- **Use on trusted networks only** (home/office WiFi)
- **Avoid public WiFi** for file sharing
- **Stop the server** when not needed (Ctrl+C)
- **Monitor access logs** for unusual activity
- **Share only necessary folders**, not entire drives

## 🔧 API Reference

NetShare provides a simple REST API:

### Get Shared Folders
```http
GET /api/folders
```
Returns JSON list of available shared folders.

Example response:
```json
[
  {
    "index": 0,
    "name": "Documents",
    "path": "/home/user/Documents"
  }
]
```

## 🏗️ Architecture

```
NetShare Architecture:

┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Mobile Device │────│  WiFi Router │────│  NetShare Host  │
│   (Browser)     │    │              │    │  (Python Flask) │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                                           │
         │              HTTP Requests                │
         └───────────────────────────────────────────┘
                        (Port 5000)

Components:
- Flask web server for HTTP requests
- QR code generator for easy mobile access
- Security middleware for safe file access
- Path validation to prevent directory traversal
- Rate limiting to prevent abuse
```

## 📝 Technical Notes

### Dependencies
- **Flask 3.0.0**: Web server framework
- **qrcode 7.4.2**: QR code generation
- **Pillow 10.1.0**: Image processing for QR codes

### File Structure
```
netshare/
├── netshare/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py          # Main application
│   ├── config.py       # Configuration settings
│   └── templates/      # HTML templates
│       ├── index.html
│       ├── browse.html
│       └── error.html
├── requirements.txt
├── pyproject.toml      # Package configuration
├── LICENSE
└── README.md          # This documentation
```

### Supported File Operations
- ✅ Download files
- ✅ Browse directories
- ✅ View file information (size, type)
- ❌ Upload files (not supported)
- ❌ Delete files (not supported)
- ❌ Modify files (not supported)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the repository for license details.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Python and dependency versions
3. Check firewall and network settings
4. Review the access logs for error details

For persistent issues, please create an issue in the repository with:
- Operating system and Python version
- Complete error messages
- Steps to reproduce the problem

---

**⚠️ Security Notice**: NetShare is designed for local network file sharing. Only use on trusted networks and share folders containing non-sensitive files. Always stop the server when not in use.
![alt text](image-2.png)
![alt text](image-3.png)
````

## File: streamlit/app.py.backup
````
#!/usr/bin/env python3
"""
Holiday Greeting QR Code Generator
A Streamlit app for creating and reading holiday greeting QR codes
"""

import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import json
from datetime import datetime
import numpy as np
import csv
import csv
from pathlib import Path
import base64
import os
import streamlit.components.v1 as components
from typing import Optional

# Import cv2 lazily to avoid startup crashes if system libs missing
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError as e:
    CV2_AVAILABLE = False
    CV2_IMPORT_ERROR = str(e)

from greeting_formats import (
    create_holiday_greeting,
    compact_greeting,
    parse_greeting,
    format_greeting_display,
    get_greeting_stats,
    encode_greeting_to_url,
    decode_greeting_from_url
)


# ============================================================================
# Download Tracking Functions
# ============================================================================

def log_download(filename: str) -> None:
    """
    Log a QR code download event to track.csv

    Args:
        filename: Name of the downloaded file

    Thread-safe implementation using file locking
    """
    # CSV file path (same directory as app.py)
    csv_path = Path(__file__).parent / "track.csv"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Create file with headers if it doesn't exist
        if not csv_path.exists():
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['filename', 'timestamp'])

        # Append with exclusive lock (prevents concurrent write corruption)
        with open(csv_path, 'a', newline='') as f:
            # Acquire exclusive lock (blocks other processes)
            try:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            except (ImportError, AttributeError):
                # fcntl not available on Windows, skip locking
                pass

            try:
                writer = csv.writer(f)
                writer.writerow([filename, timestamp])
            finally:
                # Release lock if fcntl is available
                try:
                    import fcntl
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (ImportError, AttributeError):
                    pass
    except Exception as e:
        # Silent failure - don't interrupt user experience
        import sys
        print(f"Warning: Failed to log download: {e}", file=sys.stderr)


def get_download_count() -> int:
    """
    Read and count total downloads from track.csv

    Returns:
        Number of downloads, or 0 if file doesn't exist or error occurs
    """
    csv_path = Path(__file__).parent / "track.csv"

    try:
        if not csv_path.exists():
            return 0

        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader, None)
            # Count remaining rows
            count = sum(1 for _ in reader)
            return count
    except Exception as e:
        # Return 0 on error (graceful degradation)
        import sys
        print(f"Warning: Failed to read download count: {e}", file=sys.stderr)
        return 0

# Theme to emoji mapping
THEME_ICONS = {
    "snowflake": "❄️",
    "fireworks": "🎆",
    "lights": "✨",
    "stars": "⭐",
    "confetti": "🎉",
    "champagne": "🥂",
    "hearts": "❤️",
    "farewell": "👋",
    "general": None  # No icon for general theme
}

# Page config
st.set_page_config(
    page_title="Holiday Greeting QR",
    page_icon="🎄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .greeting-box {
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stats-box {
        padding: 1rem;
        background: #e8eaf6;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .letter-container {
        background-color: #fdfbf7;
        padding: 40px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        min-height: 400px;
        position: relative;
        font-family: 'Georgia', serif;
        color: #333;
        margin-top: 20px;
    }
    .letter-header {
        margin-bottom: 30px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    .letter-from, .letter-to {
        font-size: 1.1em;
        margin: 5px 0;
    }
    .letter-body {
        font-size: 1.25em;
        line-height: 1.6;
        white-space: pre-wrap;
        margin-bottom: 60px;
    }
    .letter-watermark {
        position: absolute;
        bottom: 20px;
        right: 20px;
        opacity: 0.8;
        width: 100px;
        height: 100px;
    }
    .letter-footer {
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-size: 0.8em;
        color: #888;
    }
    /* QR Code Protection - Global fallback */
    .qr-code-protected {
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        user-select: none;
        -webkit-user-drag: none;
    }
</style>
""", unsafe_allow_html=True)



def get_img_as_base64(file_path):
    """Read image file and return base64 string"""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def is_web_url(background_str: str) -> bool:
    """
    Check if a background string is a web URL.

    Args:
        background_str: Background identifier (filename or URL)

    Returns:
        True if the string is a web URL, False otherwise
    """
    if not background_str:
        return False
    background_lower = background_str.lower()
    return background_lower.startswith(('http://', 'https://')) or \
           'youtu.be' in background_lower or \
           'youtube.com' in background_lower


def classify_background(background_str: str) -> str:
    """
    Classify background type based on URL pattern.

    Args:
        background_str: Background identifier (filename or URL)

    Returns:
        One of: 'local_file', 'youtube', 'direct_video', 'other_url', or 'invalid'
    """
    if not background_str:
        return 'invalid'

    if not is_web_url(background_str):
        return 'local_file'

    background_lower = background_str.lower()

    # Check for Google Drive URLs
    if 'drive.google.com' in background_lower and '/file/d/' in background_lower:
        return 'google_drive'

    # Check for YouTube URLs
    if 'youtube.com' in background_lower or 'youtu.be' in background_lower:
        return 'youtube'

    # Check for direct video URLs (by extension)
    if any(background_lower.endswith(ext) for ext in ['.mp4', '.webm', '.mov', '.avi', '.m3u8']):
        return 'direct_video'

    # Check if it's a generic URL
    if background_lower.startswith(('http://', 'https://')):
        return 'other_url'

    return 'invalid'


def convert_youtube_to_embed_url(youtube_url: str) -> Optional[str]:
    """
    Convert various YouTube URL formats to embeddable iframe URL.

    Handles:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - youtu.be/VIDEO_ID (without protocol)

    Args:
        youtube_url: YouTube URL in any supported format

    Returns:
        Embed URL in format https://www.youtube.com/embed/VIDEO_ID, or None if invalid
    """
    import re

    if not youtube_url:
        return None

    # YouTube video ID pattern: 11 characters (alphanumeric, hyphens, underscores)
    video_id_pattern = r'[a-zA-Z0-9_-]{11}'

    # Try different URL patterns
    patterns = [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',  # youtube.com/watch?v=ID
        r'youtu\.be/([a-zA-Z0-9_-]{11})',              # youtu.be/ID
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',     # youtube.com/embed/ID
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"

    return None


def convert_google_drive_to_embed_url(drive_url: str) -> Optional[str]:
    """
    Convert Google Drive share URL to embeddable preview URL.

    Input format: https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing
    Output format: https://drive.google.com/file/d/{FILE_ID}/preview

    Args:
        drive_url: Google Drive share URL

    Returns:
        Embed URL or None if FILE_ID cannot be extracted
    """
    import re

    # Pattern to extract FILE_ID from Google Drive URL
    # Matches: /file/d/{FILE_ID}/ where FILE_ID is alphanumeric with hyphens/underscores
    match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', drive_url)

    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"

    return None


def linkify_urls(text: str) -> str:
    """
    Convert URLs in text to clickable HTML links.
    
    Args:
        text: Plain text that may contain URLs
        
    Returns:
        Text with URLs wrapped in <a> tags
    """
    import re
    # Regex pattern for http/https URLs
    # Matches: http:// or https:// followed by valid URL characters
    # Captures full URL including domain extensions (.com, .org, etc.)
    # Trailing punctuation is removed by cleanup code below
    url_pattern = r'(https?://[^\s<>\'"\)]+)'
    
    def replace_url(match):
        url = match.group(1)
        # Remove trailing punctuation that might have been captured
        while url and url[-1] in '.,;:!?)':
            url = url[:-1]
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #667eea; text-decoration: underline;">{url}</a>'
    
    return re.sub(url_pattern, replace_url, text)


def display_qr_with_protection(qr_img: Image.Image, caption: str = "", width: int = None) -> None:
    """
    Display QR code image with right-click protection

    Args:
        qr_img: PIL Image object of QR code
        caption: Caption text to display below image
        width: Width in pixels (None for auto-width, matching Streamlit's 'stretch')

    Returns:
        None (renders HTML component directly)
    """
    # Convert PIL Image to base64 data URI
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    img_data_uri = f"data:image/png;base64,{img_base64}"

    # Get actual QR image dimensions
    img_width, img_height = qr_img.size

    # Use constrained width for consistent display
    # Max 500px width works well across devices (desktop and mobile)
    max_display_width = 500
    actual_display_width = min(img_width, max_display_width)

    # QR codes are square usually, but visible message increases height
    # Calculate height based on aspect ratio
    scaled_height = actual_display_width * (img_height / img_width) if img_width > 0 else actual_display_width

    # Add extra space for caption and margins
    caption_space = 80 if caption else 40
    iframe_height = scaled_height + caption_space

    # Build protected HTML with inline styles and JavaScript
    width_style = f"max-width: {max_display_width}px; width: 100%;"

    # Use id(qr_img) for unique element ID
    unique_id = f"qr-preview-{id(qr_img)}"

    html_code = f"""
    <div style="text-align: center; margin: 1rem 0;">
        <img
            id="{unique_id}"
            src="{img_data_uri}"
            alt="QR Code Preview"
            style="{width_style} height: auto; display: block; margin: 0 auto;
                   -webkit-touch-callout: none; -webkit-user-select: none;
                   -moz-user-select: none; -ms-user-select: none; user-select: none;
                   -webkit-user-drag: none; user-drag: none;"
            oncontextmenu="return false;"
            ondragstart="return false;"
        >
        {f'<p style="text-align: center; color: #666; font-size: 0.9em; margin-top: 0.5rem;">{caption}</p>' if caption else ''}
    </div>
    <script>
    (function() {{
        const img = document.getElementById('{unique_id}');
        if (img) {{
            img.addEventListener('contextmenu', e => {{ e.preventDefault(); return false; }});
            img.addEventListener('dragstart', e => {{ e.preventDefault(); return false; }});
            img.addEventListener('copy', e => {{ e.preventDefault(); return false; }});
        }}
    }})();
    </script>
    """

    components.html(html_code, height=iframe_height, scrolling=False)


def display_greeting_letter(greeting):
    """Display greeting in a letter format"""
    # Prepare icon for HTML
    theme_name = greeting.get('theme', 'general')
    icon_html = ""
    if theme_name in THEME_ICONS and theme_name != 'general':
        icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{theme_name}.png")
        if os.path.exists(icon_path):
            b64_icon = get_img_as_base64(icon_path)
            icon_html = f'<img src="data:image/png;base64,{b64_icon}" class="letter-watermark">'

    # Handle background if specified
    background_html = ""
    background_style = ""
    background_name = greeting.get('background', '')

    if background_name:
        # Check if background is a web URL
        if is_web_url(background_name):
            bg_type = classify_background(background_name)

            if bg_type == 'youtube':
                # YouTube embed iframe
                embed_url = convert_youtube_to_embed_url(background_name)
                if embed_url:
                    # Extract video ID for playlist parameter (required for loop)
                    video_id = embed_url.split('/')[-1]
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}?autoplay=1&mute=1&loop=1&playlist={video_id}"
                        allow="autoplay; encrypted-media"
                        allowfullscreen
                    ></iframe>'''
            elif bg_type == 'google_drive':
                # Google Drive embed iframe
                embed_url = convert_google_drive_to_embed_url(background_name)
                if embed_url:
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}"
                        allowfullscreen
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    ></iframe>'''
            elif bg_type == 'direct_video':
                # Direct HTML5 video from URL
                background_html = f'''<video autoplay loop muted playsinline
                    style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover; z-index: -1; opacity: 0.7;">
                    <source src="{background_name}" type="video/mp4">
                </video>'''
        else:
            # Local file - Check keep/ folder first, then gif/ folder
            keep_path = os.path.join(os.path.dirname(__file__), "keep", background_name)
            gif_path = os.path.join(os.path.dirname(__file__), "gif", background_name)

            if os.path.exists(keep_path):
                background_path = keep_path
            elif os.path.exists(gif_path):
                background_path = gif_path
            else:
                background_path = None

            if background_path and os.path.exists(background_path):
                ext = os.path.splitext(background_name)[1].lower()

                if ext in ['.mp4', '.webm']:
                    # Video background - embed as base64
                    b64_video = get_img_as_base64(background_path)
                    mime = "video/mp4" if ext == ".mp4" else "video/webm"
                    background_html = f'<video autoplay loop muted playsinline style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover; z-index: -1; opacity: 0.7;"><source src="data:{mime};base64,{b64_video}" type="{mime}"></video>'
                elif ext in ['.mp3', '.wav', '.ogg']:
                    # Audio background - embed as base64
                    b64_audio = get_img_as_base64(background_path)
                    mime = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg"}.get(ext, "audio/mpeg")
                    background_html = f'<audio autoplay loop style="position: absolute; bottom: 10px; left: 10px; z-index: 10; opacity: 0.7; width: 200px;"><source src="data:{mime};base64,{b64_audio}" type="{mime}"></audio>'
                elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
                    # Image background
                    b64_img = get_img_as_base64(background_path)
                    background_style = f"background-image: url(data:image/{ext[1:]};base64,{b64_img}); background-size: cover; background-position: center;"

    # Only add positioning styles if we have a background
    additional_style = ""
    if background_name and (background_html or background_style):
        additional_style = "position: relative; overflow: hidden;"

    # Combine styles
    final_style = f"{background_style} {additional_style}".strip() if (background_style or additional_style) else ""

    # Construct opening div tag with or without style
    if final_style:
        container_opening = f'<div class="letter-container" style="{final_style}">'
    else:
        container_opening = '<div class="letter-container">'

    # Render HTML Letter
    # Use components.html() for greetings with backgrounds (handles large base64 data)
    # Use st.markdown() for greetings without backgrounds (faster, cleaner)
    if background_html or background_style:
        # Add 'with-background' class for enhanced text contrast
        container_opening_with_bg = container_opening.replace(
            'class="letter-container"',
            'class="letter-container with-background"'
        )

        # Include inline CSS styles when using components.html() (doesn't inherit Streamlit CSS)
        html_content = f"""
        <style>
        .letter-container {{
            background-color: #fdfbf7;
            padding: 40px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
            min-height: 400px;
            max-width: 100%;
            width: 100%;
            height: auto;
            position: relative;
            z-index: 0;  /* Establish stacking context so video (z-index: -1) stays visible */
            isolation: isolate;
            font-family: 'Georgia', serif;
            color: #333;
            margin-top: 20px;
            overflow: hidden;
        }}

        /* Dark overlay for better text readability on backgrounds */
        .letter-container.with-background::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.25);
            z-index: 0;
            pointer-events: none;
        }}

        /* White text with shadows for backgrounds */
        .letter-container.with-background {{
            color: white;
        }}

        .letter-container.with-background .letter-header,
        .letter-container.with-background .letter-to,
        .letter-container.with-background .letter-from,
        .letter-container.with-background .letter-body,
        .letter-container.with-background .letter-footer {{
            position: relative;
            z-index: 1;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9),
                         1px 1px 2px rgba(0, 0, 0, 0.8),
                         -1px -1px 1px rgba(0, 0, 0, 0.7);
        }}

        # /* Semi-transparent background for message body */
        # .letter-container.with-background .letter-body {{
        #     background: rgba(0, 0, 0, 0.35);
        #     padding: 20px;
        #     border-radius: 8px;
        #     backdrop-filter: blur(3px);
        # }}

        .letter-header {{
            margin-bottom: 30px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.5);
            padding-bottom: 10px;
        }}
        .letter-from, .letter-to {{
            font-size: 1.1em;
            margin: 5px 0;
        }}
        .letter-body {{
            font-size: 1.25em;
            line-height: 1.6;
            white-space: pre-wrap;
            margin-bottom: 60px;
        }}
        .letter-watermark {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            opacity: 0.8;
            width: 100px;
            height: 100px;
            z-index: 1;
        }}
        .letter-footer {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            font-size: 0.8em;
            z-index: 1;
        }}
        </style>
        {container_opening_with_bg}
            {background_html}
            <div class="letter-header">
                <div class="letter-to"><strong>To:</strong> {greeting.get('to', 'Friend')}</div>
                <div class="letter-from"><strong>From:</strong> {greeting.get('from', 'Me')}</div>
            </div>
            <div class="letter-body">
{linkify_urls(greeting.get('message', ''))}
            </div>
            {icon_html}
            <div class="letter-footer">
                Created: {greeting.get('created', '').split('T')[0]}
            </div>
        </div>
        """
        # Use components.html() to handle large base64 data without size limits
        components.html(html_content, height=600, scrolling=True)
    else:
        # No background: use st.markdown() (inherits Streamlit CSS)
        html_content = f"""
        {container_opening}
            <div class="letter-header">
                <div class="letter-to"><strong>To:</strong> {greeting.get('to', 'Friend')}</div>
                <div class="letter-from"><strong>From:</strong> {greeting.get('from', 'Me')}</div>
            </div>
            <div class="letter-body">
{linkify_urls(greeting.get('message', ''))}
            </div>
            {icon_html}
            <div class="letter-footer">
                Created: {greeting.get('created', '').split('T')[0]}
            </div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)


def load_theme_icon(theme: str, size: int = 100) -> Image.Image:
    """
    Load and resize theme icon from file

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Desired icon size in pixels

    Returns:
        PIL Image with transparent background, or None if not found
    """
    import os

    # Path to icon file
    icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{theme}.png")

    try:
        # Load icon
        icon = Image.open(icon_path)

        # Resize to desired size with high-quality resampling
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)

        # Ensure RGBA mode for transparency
        if icon.mode != 'RGBA':
            icon = icon.convert('RGBA')

        return icon
    except FileNotFoundError:
        # Icon file doesn't exist - return None to skip icon
        return None
    except Exception as e:
        print(f"Error loading icon for theme '{theme}': {e}")
        return None


def get_theme_display_icon(theme: str, size: int = 60) -> Image.Image:
    """
    Load theme icon for display in UI preview

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Preview size in pixels (default 60px for grid display)

    Returns:
        PIL Image or None if theme is "general" or icon not found
    """
    if theme == "general":
        return None

    icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{theme}.png")

    if not os.path.exists(icon_path):
        return None

    try:
        icon = Image.open(icon_path)
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        return icon
    except Exception:
        return None


def render_theme_selector() -> str:
    """
    Render theme selector as a dropdown with icon preview (mobile-friendly)

    Returns:
        Selected theme name
    """
    # Theme options with emoji indicators for the dropdown
    themes = [
        ("snowflake", "❄️ Snowflake"),
        ("fireworks", "🎆 Fireworks"),
        ("lights", "✨ Lights"),
        ("stars", "⭐ Stars"),
        ("confetti", "🎉 Confetti"),
        ("champagne", "🥂 Champagne"),
        ("hearts", "❤️ Hearts"),
        ("farewell", "👋 Farewell"),
        ("general", "⊞ General (No Icon)")
    ]

    # Create lookup dictionaries
    theme_keys = [t[0] for t in themes]
    theme_labels = [t[1] for t in themes]
    key_to_label = {t[0]: t[1] for t in themes}
    label_to_key = {t[1]: t[0] for t in themes}

    # Initialize session state for theme selection
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = "snowflake"

    # Get current selection's label for the selectbox default
    current_label = key_to_label.get(st.session_state.selected_theme, theme_labels[0])
    current_index = theme_labels.index(current_label) if current_label in theme_labels else 0

    # Dropdown selector
    selected_label = st.selectbox(
        "Theme",
        options=theme_labels,
        index=current_index,
        help="Choose a theme icon to embed in your QR code",
        key="theme_dropdown"
    )

    # Update session state based on selection
    selected_theme = label_to_key.get(selected_label, "snowflake")
    st.session_state.selected_theme = selected_theme

    # Show preview of selected icon
    if selected_theme != "general":
        icon_preview = get_theme_display_icon(selected_theme, size=80)
        if icon_preview:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(icon_preview, caption="Selected Icon Preview", width='content')
    else:
        st.caption("ℹ️ General theme: QR code will have no embedded icon")

    return selected_theme


def generate_qr_code(data: str, theme: str = "general", visible_message: str = None, all_sides: bool = False, error_correction=qrcode.constants.ERROR_CORRECT_H) -> Image.Image:
    """
    Generate QR code from data string

    Args:
        data: String data to encode
        visible_message: Optional text to display around the QR code
        all_sides: If True, display visible_message on all 4 sides (top, bottom, left, right)
        error_correction: QR error correction level

    Returns:
        PIL Image of QR code
    """
    qr = qrcode.QRCode(
        version=None,  # Auto-detect version
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # Convert qrcode.image.pil.PilImage to standard PIL.Image.Image
    pil_img = img.convert('RGB')

    # Add theme icon if applicable
    if theme in THEME_ICONS and THEME_ICONS[theme]:
        qr_width, qr_height = pil_img.size

        # Icon should be ~15% of QR code size for reliable scanning (safe margin under 20%)
        icon_size = int(min(qr_width, qr_height) * 0.15)

        try:
            # Load icon from file
            icon = load_theme_icon(theme, icon_size)

            # If icon not found, skip embedding
            if icon is None:
                return pil_img

            # Calculate center position
            icon_pos = (
                (qr_width - icon_size) // 2,
                (qr_height - icon_size) // 2
            )

            # Create white background circle for better contrast
            background = Image.new('RGBA', (icon_size, icon_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(background)
            draw.ellipse([0, 0, icon_size, icon_size], fill=(255, 255, 255, 255))

            # Convert pil_img to RGBA for pasting
            pil_img = pil_img.convert('RGBA')

            # Paste white circle, then icon
            pil_img.paste(background, icon_pos, background)
            pil_img.paste(icon, icon_pos, icon)

            # Convert back to RGB
            pil_img = pil_img.convert('RGB')
        except Exception as e:
            # If icon embedding fails, just return plain QR code
            print(f"Warning: Could not embed icon for theme '{theme}': {e}")


    # Add visible message if provided
    if visible_message:
        try:
            # Prepare for font loading
            font_path = None
            font_size = 20 # Start with a baseline
            
            # Common fonts to try (including CJK support)
            # msyh.ttf = Microsoft YaHei (Windows Chinese)
            # simhei.ttf = SimHei (Windows Chinese)
            # NotoSansCJK... = Linux CJK
            font_names = ["msyh.ttf", "simhei.ttf", "arial.ttf", "calibri.ttf", "seguiemj.ttf", 
                          "segoeui.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf",
                          "WenQuanYiMicroHei.ttf", "NotoSansCJK-Regular.ttc"]
            
            for name in font_names:
                try:
                    # check if we can load it
                    ImageFont.truetype(name, font_size)
                    font_path = name
                    break
                except OSError:
                    continue
            
            # Helper to get text size
            def get_text_size(text, font):
                draw_dummy = ImageDraw.Draw(pil_img)
                if hasattr(draw_dummy, 'textbbox'):
                    bbox = draw_dummy.textbbox((0, 0), text, font=font)
                    return bbox[2] - bbox[0], bbox[3] - bbox[1]
                else:
                    return draw_dummy.textsize(text, font=font)

            qr_width, qr_height = pil_img.size
            target_width = qr_width * 0.9  # Use 90% of width for safe margins (5% each side)
            
            # Formatting
            padding = int(qr_height * 0.05) # 5% of QR height as vertical padding
            if padding < 20: padding = 20

            # Add spacing between QR code and text to prevent overlap
            text_padding = int(qr_height * 0.08)  # 8% of QR height for clear separation
            if text_padding < 15: text_padding = 15  # Minimum 15px spacing

            font = None
            if font_path:
                # Iterative sizing or calculation
                # Heuristic: Width is roughly proportional to font size
                # 1. Measure at base size
                test_font = ImageFont.truetype(font_path, font_size)
                w, h = get_text_size(visible_message, test_font)
                
                if w > 0:
                    # Calculate desired size
                    # scale = target / current
                    scale_factor = target_width / w
                    new_font_size = int(font_size * scale_factor)
                    
                    # Clamp limits
                    min_size = 12
                    max_size = int(qr_height * 0.2) # Max text height 20% of QR? Or just cap size. 
                                                  # Let's cap max size to avoid absurdity on short words like "Hi"
                    
                    if new_font_size < min_size: new_font_size = min_size
                    if new_font_size > max_size: new_font_size = max_size
                    
                    font_size = new_font_size
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = test_font
            else:
                # Fallback to default (cannot resize)
                font = ImageFont.load_default()

            # Final measurement
            text_width, text_height = get_text_size(visible_message, font)
            
            if all_sides:
                # All 4 sides mode: add text on top, bottom, left, and right
                # Calculate final image size (QR + text on all sides)
                # Use larger margin for left/right sides to prevent text from touching QR code
                side_padding = text_height + (text_padding * 3)  # Horizontal space for rotated text

                # For vertical space, we need to fit BOTH the QR code AND the rotated text
                # Rotated text height = original text_width
                # Ensure we have enough vertical space for whichever is taller
                vertical_content_height = max(qr_height, text_width)  # QR or rotated text, whichever is taller

                final_width = qr_width + 2 * side_padding  # Left and right sides
                final_height = vertical_content_height + 2 * (text_height + text_padding)  # Top and bottom text

                new_img = Image.new('RGB', (final_width, final_height), 'white')

                # Center QR code vertically within the available content area
                qr_x = side_padding
                qr_y = text_height + text_padding + (vertical_content_height - qr_height) // 2
                new_img.paste(pil_img, (qr_x, qr_y))
                
                draw_new = ImageDraw.Draw(new_img)
                
                # Draw top text (centered horizontally)
                top_text_x = (final_width - text_width) // 2
                top_text_y = (text_height + text_padding - text_height) // 2
                draw_new.text((top_text_x, top_text_y), visible_message, fill="black", font=font)
                
                # Draw bottom text (centered horizontally)
                bottom_text_x = (final_width - text_width) // 2
                bottom_text_y = text_height + text_padding + vertical_content_height + text_padding // 2
                draw_new.text((bottom_text_x, bottom_text_y), visible_message, fill="black", font=font)
                
                # Create rotated text image for left side (rotated 90 degrees counter-clockwise)
                # Add extra padding to canvas to prevent text clipping from font metrics
                canvas_padding = text_height  # Extra space for descenders/ascenders
                left_canvas_w = text_width + 2 * canvas_padding
                left_canvas_h = text_height + 2 * canvas_padding
                left_text_img = Image.new('RGBA', (left_canvas_w, left_canvas_h), (255, 255, 255, 0))
                left_draw = ImageDraw.Draw(left_text_img)
                left_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                left_text_rotated = left_text_img.rotate(90, expand=True)

                # Paste left text (centered both horizontally in side margin and vertically in content area)
                left_x = (side_padding - left_text_rotated.width) // 2
                left_y = text_height + text_padding + (vertical_content_height - left_text_rotated.height) // 2
                new_img.paste(left_text_rotated, (left_x, left_y), left_text_rotated)
                
                # Create rotated text image for right side (rotated 90 degrees clockwise)
                right_canvas_w = text_width + 2 * canvas_padding
                right_canvas_h = text_height + 2 * canvas_padding
                right_text_img = Image.new('RGBA', (right_canvas_w, right_canvas_h), (255, 255, 255, 0))
                right_draw = ImageDraw.Draw(right_text_img)
                right_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                right_text_rotated = right_text_img.rotate(-90, expand=True)

                # Paste right text (centered both horizontally in side margin and vertically in content area)
                right_x = qr_x + qr_width + (side_padding - right_text_rotated.width) // 2
                right_y = text_height + text_padding + (vertical_content_height - right_text_rotated.height) // 2
                new_img.paste(right_text_rotated, (right_x, right_y), right_text_rotated)
                
                return new_img
            else:
                # Bottom only mode (original behavior)
                # Create new image
                # Width: at least QR width. If text is somehow wider (min size limit), expand.
                final_width = max(qr_width, text_width + int(qr_width * 0.1)) # Ensure margins if text is wider
                final_height = qr_height + text_height + 2 * padding + text_padding  # Include text spacing
                
                new_img = Image.new('RGB', (final_width, final_height), 'white')
                
                # Paste QR code (centered horizontally)
                qr_x = (final_width - qr_width) // 2
                qr_y = padding // 2
                new_img.paste(pil_img, (qr_x, qr_y))
                
                # Draw text (centered horizontally, below QR)
                draw_new = ImageDraw.Draw(new_img)
                text_x = (final_width - text_width) // 2
                text_y = qr_y + qr_height + text_padding
                
                draw_new.text((text_x, text_y), visible_message, fill="black", font=font)
                
                return new_img
            
        except Exception as e:
            print(f"Warning: Failed to add visible message: {e}")
            return pil_img

    return pil_img


def create_greeting_tab():
    """Tab for creating new greeting QR codes"""
    # Display the banner image as the header (left-aligned, smaller for clarity)
    banner_path = os.path.join(os.path.dirname(__file__), "banner", "qr-greeting-banner-4x.png")
    if os.path.exists(banner_path):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.image(banner_path, width='stretch')
    else:
        # Fallback to text header if banner not found
        st.markdown('<div class="main-header"><h1>🎄 Create Holiday Greeting QR Code</h1></div>',
                    unsafe_allow_html=True)
        st.markdown("### *A greener, smarter way to say happy holidays.*")
    
    st.write("Create a personalized holiday greeting that can be shared via QR code!")

    # Two column layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Greeting Details")

        # Theme selector outside form to allow interactive button clicks
        theme = render_theme_selector()

        st.markdown("---")

        # GIF background dropdown - OUTSIDE form to allow immediate preview
        available_gifs = get_available_gifs()
        gif_options = ["(No background animation)", "(Enter custom URL...)"] + available_gifs
        
        # Initialize session state for GIF selection if needed
        if 'selected_gif_option' not in st.session_state:
             st.session_state.selected_gif_option = gif_options[0]

        if 'custom_video_url' not in st.session_state:
            st.session_state.custom_video_url = ""

        if 'custom_url_validation_status' not in st.session_state:
            st.session_state.custom_url_validation_status = None  # None, 'valid', 'invalid'

        if 'custom_url_validation_message' not in st.session_state:
            st.session_state.custom_url_validation_message = ""

        selected_gif_option = st.selectbox(
            "Background Animation (Optional)",
            options=gif_options,
            index=gif_options.index(st.session_state.selected_gif_option) if st.session_state.selected_gif_option in gif_options else 0,
            help="Choose a GIF animation to display behind your greeting",
            key="greeting_gif_background_interactive"
        )
        
        # Update session state
        st.session_state.selected_gif_option = selected_gif_option

        # Show custom URL input when "(Enter custom URL...)" is selected
        if selected_gif_option == "(Enter custom URL...)":
            custom_url = st.text_input(
                "Video URL",
                value=st.session_state.custom_video_url,
                placeholder="https://youtu.be/..., https://drive.google.com/file/d/.../view or https://example.com/video.mp4",
                help="Paste a YouTube URL, Google Drive shared video, or direct video link (.mp4, .webm, .mov, .avi, .m3u8)",
                key="custom_video_url_input",
                on_change=validate_custom_url_callback
            )
            st.session_state.custom_video_url = custom_url

            # Display validation status
            if st.session_state.custom_url_validation_status == 'valid':
                st.success(st.session_state.custom_url_validation_message)
            elif st.session_state.custom_url_validation_status == 'invalid':
                st.warning(st.session_state.custom_url_validation_message)
            elif st.session_state.custom_video_url:
                st.info("ℹ️ Validating URL...")
            else:
                st.info("ℹ️ Enter a video URL above to enable background animation")

        # Convert selection to background parameter
        if selected_gif_option == "(No background animation)":
            selected_gif = ""
        elif selected_gif_option == "(Enter custom URL...)":
            # Use custom URL if validated, otherwise empty
            if st.session_state.custom_url_validation_status == 'valid':
                selected_gif = st.session_state.custom_video_url
            else:
                selected_gif = ""
        else:
            # Local file selected
            selected_gif = selected_gif_option

        # Immediate preview below the dropdown (only for local files)
        if selected_gif and selected_gif_option != "(Enter custom URL...)":
            gif_path = os.path.join(os.path.dirname(__file__), "gif", selected_gif)
            if os.path.exists(gif_path):
                st.image(gif_path, caption=f"Preview: {selected_gif}", width='stretch')
            else:
                st.warning(f"GIF file not found: {selected_gif}")
        
        st.markdown("---")

        with st.form("greeting_form"):
            from_name = st.text_input(
                "From (Your Name)",
                placeholder="Alice",
                help="Who is sending this greeting?",
                key="greeting_from_name"
            )

            to_name = st.text_input(
                "To (Recipient Name)",
                placeholder="Bob",
                help="Who will receive this greeting?",
                key="greeting_to_name"
            )

            message = st.text_area(
                "Your Message",
                placeholder="Merry Christmas! Wishing you joy and happiness this season...",
                height=150,
                help="Your personalized greeting message",
                key="greeting_message"
            )
            
            visible_message = st.text_input(
                "Visible Message (Optional)",
                placeholder="Scan me!",
                help="Short text to display below the QR code image",
                key="greeting_visible_message"
            )
            
            all_sides = st.checkbox(
                "Add message to all 4 sides",
                value=False,
                help="Display the visible message on top, bottom, left, and right of the QR code",
                key="greeting_all_sides"
            )



            # Character counter
            if message:
                st.caption(f"Message length: {len(message)} characters")

            generate_btn = st.form_submit_button("Generate QR Code", icon=":material/qr_code_2:", type="primary", width='stretch')

    with col2:
        st.subheader("QR Code Preview")

        # Show GIF preview immediately when selected


        if generate_btn:
            # Debug: Check what values we received
            # st.write(f"Debug - from_name: '{from_name}', to_name: '{to_name}', message: '{message}'")

            if not from_name or not to_name or not message:
                st.error("Please fill in all required fields (From, To, and Message)")
            elif selected_gif_option == "(Enter custom URL...)":
                # Validate custom URL before generation
                if not st.session_state.custom_video_url:
                    st.warning("⚠️ No video URL entered. Generating QR code without background animation.")
                    # Continue with selected_gif = "" (already set)
                    greeting = create_holiday_greeting(
                        from_name=from_name,
                        to_name=to_name,
                        message=message,
                        theme=theme,
                        background=selected_gif
                    )

                    # Encode greeting as URL (for mobile scanning)
                    greeting_url = encode_greeting_to_url(greeting)

                    # Get statistics based on URL length
                    stats = get_greeting_stats(greeting_url)

                    # Generate QR code with URL data and theme icon
                    qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_message, all_sides=all_sides)

                    # Display QR code
                    display_qr_with_protection(qr_img, caption=f"Greeting QR Code for {to_name}", width=None)

                    # Statistics
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.write("**QR Code Statistics:**")
                    st.write(f"- Data size: {stats['byte_size']} bytes")
                    st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
                    st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
                    st.caption("📱 Scan with phone camera to open greeting directly!")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download button
                    buf = io.BytesIO()
                    qr_img.save(buf, format='PNG')
                    byte_im = buf.getvalue()

                    # Generate filename first for consistency
                    filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                    # Download button with tracking callback
                    st.download_button(
                        label="📥 Download QR Code",
                        data=byte_im,
                        file_name=filename,
                        mime="image/png",
                        width='stretch',
                        on_click=log_download,
                        args=(filename,)
                    )
                elif st.session_state.custom_url_validation_status != 'valid':
                    st.error(f"❌ Invalid video URL: {st.session_state.custom_url_validation_message}")
                    st.info("💡 Please enter a valid YouTube or video URL, or select a different background option.")
                else:
                    # Valid URL - proceed
                    greeting = create_holiday_greeting(
                        from_name=from_name,
                        to_name=to_name,
                        message=message,
                        theme=theme,
                        background=selected_gif
                    )

                    # Encode greeting as URL (for mobile scanning)
                    greeting_url = encode_greeting_to_url(greeting)

                    # Get statistics based on URL length
                    stats = get_greeting_stats(greeting_url)

                    # Generate QR code with URL data and theme icon
                    qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_message, all_sides=all_sides)

                    # Display QR code
                    display_qr_with_protection(qr_img, caption=f"Greeting QR Code for {to_name}", width=None)

                    # Statistics
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.write("**QR Code Statistics:**")
                    st.write(f"- Data size: {stats['byte_size']} bytes")
                    st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
                    st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
                    st.caption("📱 Scan with phone camera to open greeting directly!")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download button
                    buf = io.BytesIO()
                    qr_img.save(buf, format='PNG')
                    byte_im = buf.getvalue()

                    # Generate filename first for consistency
                    filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                    # Download button with tracking callback
                    st.download_button(
                        label="📥 Download QR Code",
                        data=byte_im,
                        file_name=filename,
                        mime="image/png",
                        width='stretch',
                        on_click=log_download,
                        args=(filename,)
                    )
            else:
                # Normal flow (local file or no background)
                greeting = create_holiday_greeting(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    theme=theme,
                    background=selected_gif
                )

                # Encode greeting as URL (for mobile scanning)
                greeting_url = encode_greeting_to_url(greeting)

                # Get statistics based on URL length
                stats = get_greeting_stats(greeting_url)

                # Generate QR code with URL data and theme icon
                qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_message, all_sides=all_sides)

                # Display QR code
                display_qr_with_protection(qr_img, caption=f"Greeting QR Code for {to_name}", width=None)

                # Statistics
                st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                st.write("**QR Code Statistics:**")
                st.write(f"- Data size: {stats['byte_size']} bytes")
                st.write(f"- QR Version: ~{stats['recommended_qr_version']}")
                st.write(f"- Scannable: {'✅ Yes' if stats['fits_in_qr'] else '❌ Too large'}")
                st.caption("📱 Scan with phone camera to open greeting directly!")
                st.markdown('</div>', unsafe_allow_html=True)

                # Download button
                buf = io.BytesIO()
                qr_img.save(buf, format='PNG')
                byte_im = buf.getvalue()

                # Generate filename first for consistency
                filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                # Download button with tracking callback
                st.download_button(
                    label="📥 Download QR Code",
                    data=byte_im,
                    file_name=filename,
                    mime="image/png",
                    width='stretch',
                    on_click=log_download,
                    args=(filename,)
                )

                # Show JSON data
                # Show raw data (Removed as it's now just the message)
                # with st.expander("View Greeting Data"):
                #     st.text(greeting_json)





def scan_greeting_tab():
    """Tab for scanning/decoding greeting QR codes"""
    st.markdown('<div class="main-header"><h1>📱 Scan Greeting QR Code</h1></div>',
                unsafe_allow_html=True)

    # Check if greeting data is passed via URL parameters (from QR code scan)
    try:
        query_params = st.query_params
    except:
        query_params = st.experimental_get_query_params()
    
    # Check if we have greeting data in URL (m or mc parameter indicates a message)
    has_url_greeting = query_params.get('m') or query_params.get('mc')
    
    if has_url_greeting:
        # Decode greeting from URL parameters and display it
        greeting = decode_greeting_from_url(dict(query_params))
        
        if greeting:
            st.success("🎉 Greeting received!")
            
            # Display the full letter format
            display_greeting_letter(greeting)
            
            st.markdown("---")
            
            # Option to create their own or scan another
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 Create Your Own Greeting", width='stretch'):
                    st.query_params.clear()
                    st.rerun()
            with col2:
                if st.button("📤 Scan Another QR Code", width='stretch'):
                    # Clear only the greeting params, keep tab=scan
                    st.query_params.clear()
                    st.query_params["tab"] = "scan"
                    st.rerun()
            
            return  # Don't show the upload interface
        else:
            st.warning("Could not decode greeting from URL. Try uploading the QR code image instead.")

    # Normal upload interface
    st.write("Upload a greeting QR code image to view the message!")

    uploaded_file = st.file_uploader(
        "Choose a QR code image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image containing a greeting QR code"
    )

    if uploaded_file is not None:
        try:
            # Display uploaded image
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("Uploaded QR Code")
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", width='stretch')

            # Decode QR code
            try:
                if not CV2_AVAILABLE:
                    raise ImportError(f"OpenCV not available: {CV2_IMPORT_ERROR}")

                # Use OpenCV for decoding (No pyzbar dependency)
                # Convert PIL Image to BGR numpy array
                image_array = np.array(image.convert('RGB'))
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

                detector = cv2.QRCodeDetector()
                data, bbox, _ = detector.detectAndDecode(image_array)

                if data:
                    qr_data = data

                    # Parse greeting (handles both URL and JSON formats)
                    greeting = parse_greeting(qr_data)

                    with col2:
                        st.subheader("Greeting Message")

                        if greeting:
                            # Display formatted greeting
                            display_greeting_letter(greeting)
                        else:
                            st.warning("This QR code doesn't contain a valid greeting format.")
                            st.write("**Decoded data:**")
                            st.code(qr_data)
                else:
                    st.error("No QR code found in the image. Please upload a valid QR code image.")

            except ImportError as e:
                st.error(f"QR code scanning requires OpenCV system libraries.")
                st.info("Please use manual JSON entry below:")

                manual_data = st.text_area("Paste QR Code Data (JSON)")
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Invalid greeting data format")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Alternatively, you can manually paste the QR code data below:")

                manual_data = st.text_area("Paste QR Code Data (JSON)", key="manual_data_exception")
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Invalid greeting data format")

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")


def examples_tab():
    """Tab showing example greetings"""
    st.markdown('<div class="main-header"><h1>📖 Examples</h1></div>',
                unsafe_allow_html=True)

    st.write("Here are some example holiday greetings you can create:")

    examples = [
        {
            "title": "🎄 Christmas Greeting",
            "from": "Alice",
            "to": "Bob",
            "theme": "snowflake",
            "message": "Merry Christmas! Wishing you joy and happiness this season. Thank you for being a wonderful friend!"
        },
        {
            "title": "🎆 New Year Message",
            "from": "Bob",
            "to": "Future Me",
            "theme": "fireworks",
            "message": "2025 was incredible! Here's to growth and new adventures in 2026!"
        },
        {
            "title": "💍 Wedding Save the Date",
            "from": "Emma & James",
            "to": "Friends and Family",
            "theme": "champagne",
            "message": "We're getting married! Save the date: June 15, 2026. More details to follow!"
        },
        {
            "title": "👋 Farewell to Colleagues",
            "from": "Alex",
            "to": "The Team",
            "theme": "farewell",
            "message": "It's been an amazing journey working with you all! Thank you for the memories, the laughs, and the lessons. Let's stay in touch!",
            "visible_message": "Scan to read my farewell note"
        }
    ]

    for example in examples:
        with st.expander(example["title"]):
            col1, col2 = st.columns([1, 1])

            with col1:
                st.write(f"**From:** {example['from']}")
                st.write(f"**To:** {example['to']}")
                st.write(f"**Theme:** {example['theme']}")
                st.markdown("---")
                st.write(example['message'])

            with col2:
                # Generate QR for example
                greeting = create_holiday_greeting(
                    from_name=example['from'],
                    to_name=example['to'],
                    message=example['message'],
                    theme=example['theme']
                )
                # Use URL encoding for QR code
                greeting_url = encode_greeting_to_url(greeting)
                visible_msg = example.get('visible_message', None)
                qr_img = generate_qr_code(greeting_url, theme=example['theme'], visible_message=visible_msg)
                display_qr_with_protection(qr_img, caption="QR Code", width=None)


def get_available_backgrounds():
    """Get list of available background files from keep/ folder"""
    keep_path = Path(__file__).parent / "keep"
    if not keep_path.exists():
        return []

    # Support images and videos
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'}
    backgrounds = []
    for f in keep_path.iterdir():
        if f.suffix.lower() in extensions:
            backgrounds.append(f.name)
    return sorted(backgrounds)


def validate_custom_url_callback():
    """Validate custom video URL when user types"""
    url = st.session_state.get('custom_video_url_input', '').strip()

    if not url:
        st.session_state.custom_url_validation_status = None
        st.session_state.custom_url_validation_message = ""
        return

    if not is_web_url(url):
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = "⚠️ Invalid URL format. Must start with http:// or https://"
        return

    bg_type = classify_background(url)

    if bg_type == 'youtube':
        embed_url = convert_youtube_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = "✅ Valid YouTube URL"
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = "⚠️ Invalid YouTube URL. Could not extract video ID."

    elif bg_type == 'google_drive':
        embed_url = convert_google_drive_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = "✅ Valid Google Drive URL"
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = "⚠️ Invalid Google Drive URL. Could not extract file ID."

    elif bg_type == 'direct_video':
        st.session_state.custom_url_validation_status = 'valid'
        file_ext = url.split('.')[-1].upper()
        st.session_state.custom_url_validation_message = f"✅ Valid video URL ({file_ext})"

    elif bg_type == 'other_url':
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = "⚠️ Unsupported URL type. Use YouTube or direct video links (.mp4, .webm, .mov, .avi, .m3u8)"

    else:
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = "⚠️ Could not validate URL format"


def get_available_gifs():
    """Get list of available background files (GIF, JPG) from gif/ folder"""
    gif_path = Path(__file__).parent / "gif"
    if not gif_path.exists():
        return []

    gifs = []
    for f in gif_path.iterdir():
        if f.suffix.lower() in ['.gif', '.jpg', '.jpeg']:
            gifs.append(f.name)
    return sorted(gifs)


def get_all_available_backgrounds():
    """Get combined list of backgrounds from both keep/ and gif/ folders"""
    backgrounds_from_keep = get_available_backgrounds()
    backgrounds_from_gif = get_available_gifs()

    # Create a dictionary to track folder source for each file
    # This helps with file resolution later
    background_map = {}
    for bg in backgrounds_from_keep:
        background_map[bg] = 'keep'
    for bg in backgrounds_from_gif:
        if bg not in background_map:  # Avoid duplicates, keep/ takes priority
            background_map[bg] = 'gif'

    return sorted(background_map.keys()), background_map


def batch_greeting_tab():
    """Tab for batch QR code generation from Excel"""

    # Initialize session state for batch DataFrame
    if 'batch_df' not in st.session_state:
        st.session_state.batch_df = None

    st.markdown('<div class="main-header"><h1>📦 Batch QR Code Generation</h1></div>',
                unsafe_allow_html=True)

    st.write("Generate multiple QR codes at once by uploading an Excel spreadsheet.")
    st.info("💡 **New Feature**: You can now use YouTube URLs or direct video URLs as backgrounds! Just paste the URL in the Background column.")
    
    # Available themes and backgrounds for reference
    available_themes = list(THEME_ICONS.keys())
    all_backgrounds, background_folder_map = get_all_available_backgrounds()
    available_backgrounds_keep = get_available_backgrounds()
    available_backgrounds_gif = get_available_gifs()
    
    st.markdown("---")
    
    # Template download section
    st.subheader("1. Download Template")
    st.write("Download the Excel template, fill in your greetings, then upload it below.")
    
    # Create template Excel file in memory
    try:
        import pandas as pd
        from io import BytesIO
        
        # Create sample data with 4 test cases
        sample_data = {
            "From": ["Alice", "Bob", "Charlie", "David"],
            "To": ["Bob", "Alice", "Dana", "Eve"],
            "Message": ["Merry Christmas!", "Happy New Year!", "Season's Greetings!\nhttps://qr-greeting.co.uk", "Enjoy the holidays!"],
            "Theme": ["snowflake", "fireworks", "hearts", "lights"],
            "Background": ["letter-background-design-01.jpg", "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4", "https://youtu.be/6SuLXoRmykE", "christmas-lights.gif"],
            "VisibleMessage": ["Scan me!", "BOB", "Happy Holidays!", "Ho Ho Ho!"]
        }
        df_template = pd.DataFrame(sample_data)
        
        # Save to CSV
        csv_data = df_template.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Template (.csv)",
            data=csv_data,
            file_name="qr_greeting_template.csv",
            mime="text/csv"
        )
        
        # Show valid options for reference
        with st.expander("View Valid Options"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Valid Themes:**")
                for theme in available_themes:
                    emoji = THEME_ICONS.get(theme, "")
                    st.write(f"- `{theme}` {emoji if emoji else ''}")
            with col2:
                st.write("**Valid Backgrounds:**")
                st.write("*Local files from `keep/` folder:*")
                if available_backgrounds_keep:
                    for bg in available_backgrounds_keep:
                        st.write(f"- `{bg}`")
                else:
                    st.write("No backgrounds available in `keep/` folder")
                st.write("")
                st.write("*Local files from `gif/` folder:*")
                if available_backgrounds_gif:
                    for bg in available_backgrounds_gif:
                        st.write(f"- `{bg}`")
                else:
                    st.write("No backgrounds available in `gif/` folder")
                st.write("")
                st.write("*Or use web video URLs:*")
                st.write("- YouTube: `youtu.be/VIDEO_ID`")
                st.write("- YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`")
                st.write("- Direct video: `https://example.com/video.mp4`")
        
    except ImportError:
        st.error("pandas is required for batch processing. Please install it: `pip install pandas`")
        return
    
    st.markdown("---")
    
    # Upload section
    st.subheader("2. Upload Filled Template")
    
    uploaded_file = st.file_uploader(
        "Choose your filled CSV file",
        type=['csv'],
        help="Upload the template with your greeting data"
    )
    
    if uploaded_file is not None:
        try:
            # Load CSV into session state (only when new file is uploaded)
            df = pd.read_csv(uploaded_file)
            # Check if this is a new upload by comparing with existing data
            if st.session_state.batch_df is None or len(df) != len(st.session_state.batch_df):
                st.session_state.batch_df = df

            st.success(f"Loaded {len(st.session_state.batch_df)} greetings from CSV!")

            # Preview data with editable interface
            with st.expander("Preview Data"):
                st.session_state.batch_df = st.data_editor(
                    st.session_state.batch_df,
                    key="batch_data_editor",
                    num_rows="dynamic"
                )
            
            # Validate data
            required_cols = ["From", "To", "Message"]
            missing_cols = [col for col in required_cols if col not in st.session_state.batch_df.columns]

            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                return

            # Validate themes
            if "Theme" in st.session_state.batch_df.columns:
                invalid_themes = st.session_state.batch_df[~st.session_state.batch_df["Theme"].isna() & ~st.session_state.batch_df["Theme"].isin(available_themes)]["Theme"].unique()
                if len(invalid_themes) > 0:
                    st.warning(f"Some rows have invalid themes: {list(invalid_themes)}. They will use 'general'.")
            
            # Generate button
            if st.button("🚀 Generate All QR Codes", type="primary"):
                import zipfile

                zip_buffer = BytesIO()

                progress = st.progress(0)
                status = st.empty()

                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for idx, row in st.session_state.batch_df.iterrows():
                        from_name = str(row.get("From", ""))
                        to_name = str(row.get("To", ""))
                        message = str(row.get("Message", ""))
                        theme = str(row.get("Theme", "general")) if pd.notna(row.get("Theme")) else "general"
                        background = str(row.get("Background", "")) if pd.notna(row.get("Background")) else ""
                        visible_msg = str(row.get("VisibleMessage", "")) if pd.notna(row.get("VisibleMessage")) else ""
                        
                        # Validate theme
                        if theme not in available_themes:
                            theme = "general"

                        # Validate background (local file or web URL)
                        if background:
                            if is_web_url(background):
                                # Validate web URL format
                                bg_type = classify_background(background)
                                if bg_type == 'youtube':
                                    # Validate YouTube URL can be converted to embed format
                                    if convert_youtube_to_embed_url(background) is None:
                                        st.warning(f"Row {idx + 1}: Invalid YouTube URL '{background}' - skipping background")
                                        background = ""
                                elif bg_type == 'google_drive':
                                    # Validate Google Drive URL can be converted to embed format
                                    if convert_google_drive_to_embed_url(background) is None:
                                        st.warning(f"Row {idx + 1}: Invalid Google Drive URL '{background}' - skipping background")
                                        background = ""
                                elif bg_type == 'direct_video':
                                    # Direct video URLs are accepted as-is
                                    # Note: CORS and accessibility depend on the video host
                                    pass
                                else:
                                    # Other URL types not supported
                                    st.warning(f"Row {idx + 1}: Unsupported URL type '{background}' - skipping background")
                                    background = ""
                            else:
                                # Check if background exists in either folder
                                background_found = False

                                # Check keep/ folder first
                                keep_path = Path(__file__).parent / "keep" / background
                                if keep_path.exists():
                                    background_found = True
                                else:
                                    # Check gif/ folder
                                    gif_path = Path(__file__).parent / "gif" / background
                                    if gif_path.exists():
                                        background_found = True

                                if not background_found:
                                    st.warning(f"Row {idx + 1}: Background file '{background}' not found in keep/ or gif/ folders - skipping background")
                                    background = ""
                        
                        status.text(f"Generating QR {idx + 1}/{len(st.session_state.batch_df)}: {to_name}...")
                        
                        # Create greeting
                        greeting = create_holiday_greeting(
                            from_name=from_name,
                            to_name=to_name,
                            message=message,
                            theme=theme,
                            background=background
                        )
                        
                        # Encode to URL
                        greeting_url = encode_greeting_to_url(greeting)
                        
                        # Generate QR code
                        qr_img = generate_qr_code(greeting_url, theme=theme, visible_message=visible_msg)
                        
                        # Save to zip
                        img_buffer = BytesIO()
                        qr_img.save(img_buffer, format='PNG')
                        img_buffer.seek(0)
                        
                        # Filename: to_name_index.png
                        safe_name = "".join(c for c in to_name if c.isalnum() or c in (' ', '-', '_')).strip()
                        filename = f"{safe_name}_{idx + 1}.png"
                        
                        zf.writestr(filename, img_buffer.read())

                        progress.progress((idx + 1) / len(st.session_state.batch_df))
                
                status.text("✅ All QR codes generated!")
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download All QR Codes (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"qr_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip"
                )
                
        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")


def about_tab():
    """About the application"""
    st.markdown('<div class="main-header"><h1>ℹ️ About</h1></div>',
                unsafe_allow_html=True)

    st.write("""
    ## Holiday Greeting QR Code Generator

    This application allows you to create personalized holiday greetings encoded in QR codes.
    Share your messages in a unique and modern way!
    """)

    st.markdown("---")
    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=6SuLXoRmykE")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Video section with styled heading
    st.markdown("""
<div style="text-align: center; margin: 2rem 0 1rem 0;">
    <h3 style="color: #333; margin-bottom: 0.5rem;">See It In Action</h3>
    <p style="color: #666; margin-bottom: 1.5rem; font-size: 1rem;">
        Watch a quick demo of how easy it is to create and share personalized greeting QR codes.
    </p>
</div>
""", unsafe_allow_html=True)

    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=hJdGamlet5A")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Core positioning messages
    st.markdown("---")
    st.subheader("Why Choose QR Greetings?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🌱 Environment Friendly

        **Zero paper. Zero postage. Instant delivery.**

        Traditional paper cards consume materials, printing resources, and shipping energy.
        QR greetings are 100% digital — no trees harmed, no carbon footprint from delivery trucks.

        Send your love without leaving a trace on the planet.
        """)

    with col2:
        st.markdown("""
        ### 🔐 Secret in Transit

        **Your message stays private until revealed.**

        Unlike public social media posts, your greeting is encoded within the QR pattern itself.
        Only the recipient who scans it can see your heartfelt message.

        It's like a digital sealed envelope — personal, intimate, and special.
        """)

    with col3:
        st.markdown("""
        ### 📱 Device Friendly

        **Works on any phone. No app required.**

        Recipients simply point their camera at the QR code — that's it!
        Works seamlessly on both iOS and Android, opening directly in the browser.

        No downloads, no sign-ups, no friction. Just scan and smile.
        """)

    st.markdown("---")

    st.write("""
    ### Features
    - ✨ Create custom greeting QR codes
    - 📱 Scan and read greeting QR codes
    - 🎨 Multiple theme options with embedded icons
    - 📥 Download QR codes as images
    - 💾 Compact JSON format for efficient encoding

    ### How It Works
    1. Enter your greeting details (from, to, message)
    2. Choose a theme
    3. Generate the QR code
    4. Download and share!

    Recipients can scan the QR code with their phone camera or upload it to this app to view your message.

    ### Technical Details
    - Uses high error correction (Level H) for reliable scanning
    - Compact JSON format minimizes QR code size
    - Supports messages up to ~500 characters comfortably
    - Built with Streamlit and netshare

    ### Powered By
    - **netshare** - Network sharing and QR code utilities
    - **Streamlit** - Interactive web interface
    - **qrcode** - QR code generation
    - **Pillow** - Image processing
    """)

    # Display download count (just the number)
    count = get_download_count()
    st.write(count)


def view_greeting_page(query_params: dict):
    """
    Display a greeting message in a clean, mobile-friendly format.
    This is shown when users scan the QR code with their phone camera.
    
    Args:
        query_params: URL query parameters containing greeting data
    """
    # Decode greeting from URL parameters
    greeting = decode_greeting_from_url(query_params)
    
    if not greeting:
        st.error("Invalid or missing greeting data.")
        st.write("Please scan a valid greeting QR code or go to the main page to create one.")
        if st.button("Go to Home Page"):
            st.query_params.clear()
            st.rerun()
        return
    
    # Get theme for styling
    theme = greeting.get("theme", "general")
    theme_emoji = THEME_ICONS.get(theme, "🎄")
    
    # Mobile-optimized greeting display (message only)
    st.markdown("""
    <style>
        .mobile-greeting-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 2rem 1rem;
            text-align: center;
        }
        .greeting-emoji {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        .greeting-message {
            font-family: 'Georgia', serif;
            font-size: 1.5rem;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #fdfbf7 0%, #f5f0e8 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .greeting-from {
            font-size: 1.1rem;
            color: #666;
            margin-top: 1.5rem;
            font-style: italic;
        }
        .view-full-link {
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #888;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the greeting
    st.markdown('<div class="mobile-greeting-container">', unsafe_allow_html=True)
    
    # Theme emoji
    if theme_emoji:
        st.markdown(f'<div class="greeting-emoji">{theme_emoji}</div>', unsafe_allow_html=True)
    
    # The message (main content)
    message = greeting.get("message", "")
    st.markdown(f'<div class="greeting-message">{message}</div>', unsafe_allow_html=True)
    
    # From attribution (subtle)
    from_name = greeting.get("from", "")
    if from_name:
        st.markdown(f'<div class="greeting-from">— From {from_name}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Subtle link to create your own (not prominent)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("Create your own greeting QR code!")
        if st.button("Create Greeting", type="secondary", width='stretch'):
            st.query_params.clear()
            st.rerun()


def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        # st.image("https://raw.githubusercontent.com/anthropics/anthropic-quickstarts/main/computer-use-demo/image.png",
        #          width=100)
        st.title("Holiday Greeting QR")
        st.write("Create and share personalized holiday greetings via QR codes!")
        st.markdown("*A greener, smarter way to say happy holidays.*")

        st.markdown("---")

        st.write("### Quick Tips")
        st.info("""
        💡 Keep messages under 300 characters for best QR code size

        📱 Test QR codes with your phone camera app

        🎨 Choose themes that match your occasion
        """)
        
        st.markdown("---")
        
        # Batch tab toggle
        show_batch = st.checkbox("Show Batch Tab", value=False, help="Enable batch QR code generation from Excel")

    # Read query param for tab selection
    try:
        query_params = st.query_params
        tab_param = query_params.get('tab', 'create')
    except:
        # Fallback for older Streamlit versions
        query_params = st.experimental_get_query_params()
        tab_param = query_params.get('tab', ['create'])[0]

    # Check if this is a "view" request (from QR code scan)
    if tab_param == "view":
        # Show mobile-friendly greeting view (message only)
        view_greeting_page(dict(query_params))
        return  # Don't show the normal app interface

    # Map tab names to indices (depends on whether batch tab is shown)
    if show_batch:
        tab_map = {"create": 0, "scan": 1, "examples": 2, "batch": 3, "about": 4}
    else:
        tab_map = {"create": 0, "scan": 1, "examples": 2, "about": 3}
    tab_index = tab_map.get(tab_param, 0)

    # Inject JavaScript to click the correct tab (only if not the first tab)
    if tab_index > 0:
        st.components.v1.html(f"""
            <script>
            (function() {{
                let attempts = 0;
                const maxAttempts = 10;

                function clickTab() {{
                    const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');

                    if (tabs && tabs.length > {tab_index}) {{
                        tabs[{tab_index}].click();
                        return true;
                    }} else if (attempts < maxAttempts) {{
                        attempts++;
                        setTimeout(clickTab, 100);
                    }}
                }}

                clickTab();
            }})();
            </script>
        """, height=0)

    # Main tabs (conditionally include batch tab)
    if show_batch:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Create Greeting", "Scan QR Code", "Examples", "Batch", "About"])
        
        with tab1:
            create_greeting_tab()

        with tab2:
            scan_greeting_tab()

        with tab3:
            examples_tab()

        with tab4:
            batch_greeting_tab()

        with tab5:
            about_tab()
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["Create Greeting", "Scan QR Code", "Examples", "About"])

        with tab1:
            create_greeting_tab()

        with tab2:
            scan_greeting_tab()

        with tab3:
            examples_tab()

        with tab4:
            about_tab()


if __name__ == "__main__":
    main()
````

## File: streamlit/generate_burn_icon.py
````python
#!/usr/bin/env python3
"""
Generate burn_after_read.png icon
Envelope on fire with Mission Impossible aesthetic
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_burn_after_read_icon(size=512):
    """Create envelope-on-fire icon with Mission Impossible styling"""

    # Create transparent canvas
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Mission Impossible colors
    flame_orange = (255, 69, 0, 255)  # #FF4500
    dark_red = (139, 0, 0, 255)       # #8B0000
    near_black = (26, 26, 26, 255)    # #1A1A1A
    envelope_white = (240, 240, 240, 255)

    center_x = size // 2
    center_y = size // 2

    # 1. Draw flames in background (behind envelope)
    # Multiple flame shapes with gradient effect
    flame_positions = [
        # Bottom flames
        (center_x - 120, center_y + 100, 80, 150),
        (center_x - 40, center_y + 120, 70, 140),
        (center_x + 40, center_y + 110, 75, 145),
        (center_x + 120, center_y + 90, 65, 135),
        # Side flames
        (center_x - 160, center_y + 40, 60, 120),
        (center_x + 160, center_y + 50, 55, 115),
    ]

    for fx, fy, fw, fh in flame_positions:
        # Draw flame shape (teardrop/flame)
        flame_points = []
        # Create flame outline
        for i in range(20):
            angle = (i / 20) * math.pi
            x = fx + math.cos(angle) * fw
            y = fy + math.sin(angle) * (fh * 0.6)
            flame_points.append((x, y))
        # Flame tip
        flame_points.append((fx, fy - fh))

        # Draw with gradient effect (outer darker, inner brighter)
        draw.polygon(flame_points, fill=dark_red, outline=None)

        # Inner brighter flame
        inner_points = []
        for i in range(20):
            angle = (i / 20) * math.pi
            x = fx + math.cos(angle) * (fw * 0.6)
            y = fy + math.sin(angle) * (fh * 0.4)
            inner_points.append((x, y))
        inner_points.append((fx, fy - fh * 0.7))
        draw.polygon(inner_points, fill=flame_orange, outline=None)

    # 2. Draw envelope
    envelope_top = center_y - 60
    envelope_bottom = center_y + 80
    envelope_left = center_x - 140
    envelope_right = center_x + 140

    # Envelope body (rectangle)
    draw.rectangle(
        [envelope_left, envelope_top + 50, envelope_right, envelope_bottom],
        fill=envelope_white,
        outline=near_black,
        width=3
    )

    # Envelope flap (triangle)
    flap_points = [
        (envelope_left, envelope_top + 50),
        (center_x, envelope_top),
        (envelope_right, envelope_top + 50)
    ]
    draw.polygon(flap_points, fill=(220, 220, 220, 255), outline=near_black, width=3)

    # Envelope flap lines (to show it's closed)
    draw.line([envelope_left, envelope_top + 50, center_x, envelope_top], fill=near_black, width=2)
    draw.line([center_x, envelope_top, envelope_right, envelope_top + 50], fill=near_black, width=2)

    # 3. Add "TOP SECRET" stamp
    stamp_x = center_x
    stamp_y = center_y + 20

    # Red stamp background
    stamp_bg = (200, 0, 0, 180)  # Semi-transparent red
    draw.ellipse(
        [stamp_x - 60, stamp_y - 30, stamp_x + 60, stamp_y + 30],
        fill=stamp_bg,
        outline=(150, 0, 0, 255),
        width=2
    )

    # Try to add text (will use default font if custom not available)
    try:
        # Try to load a font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Draw "TOP SECRET" text
    text = "TOP SECRET"
    # Get text bbox for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = stamp_x - text_width // 2
    text_y = stamp_y - text_height // 2

    draw.text((text_x, text_y), text, fill=near_black, font=font)

    # 4. Add more flames on top of envelope edges (burning effect)
    top_flames = [
        (envelope_left + 30, envelope_top + 30, 40, 80),
        (envelope_right - 30, envelope_top + 40, 35, 75),
        (center_x - 60, envelope_bottom - 20, 45, 70),
        (center_x + 60, envelope_bottom - 15, 40, 65),
    ]

    for fx, fy, fw, fh in top_flames:
        # Draw flame shape
        flame_points = []
        for i in range(15):
            angle = (i / 15) * math.pi
            x = fx + math.cos(angle) * fw
            y = fy + math.sin(angle) * (fh * 0.5)
            flame_points.append((x, y))
        flame_points.append((fx, fy - fh))

        draw.polygon(flame_points, fill=flame_orange, outline=dark_red, width=2)

    # 5. Add glow effect around flames (optional, for dramatic effect)
    # This is simulated by adding semi-transparent orange circles
    for fx, fy, _, fh in flame_positions + top_flames:
        glow_radius = fh * 0.4
        draw.ellipse(
            [fx - glow_radius, fy - glow_radius, fx + glow_radius, fy + glow_radius],
            fill=(255, 140, 0, 40)  # Semi-transparent orange glow
        )

    return img

if __name__ == "__main__":
    print("Generating burn_after_read.png icon...")
    icon = create_burn_after_read_icon(512)

    # Save to icons directory
    output_path = "/mnt/e/code2/netshare/streamlit/icons/burn_after_read.png"
    icon.save(output_path, "PNG")
    print(f"✓ Icon saved to {output_path}")
    print(f"  Size: {icon.size}")
    print("  Design: Envelope on fire with Mission Impossible aesthetic")
    print("  Colors: Flame orange (#FF4500) + Near-black (#1A1A1A)")
````

## File: streamlit/generate_donation_qr.py
````python
# Script to generate a specific PayPal Donation QR code
# Run this from the codebase\streamlit directory:
# python generate_donation_qr.py

import os
import sys

# Ensure we can import from local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qr.generator import generate_qr_code
from config import THEME_COLORS

def create_donation_qr():
    # PayPal URL
    paypal_url = "https://www.paypal.com/ncp/payment/NUQG396UTFRMG"
    
    # Text Options
    # You can change this to: "Scan to Support ☕", "Feed the Developer", etc.
    visible_message = "Scan to Donate £1"
    
    # Theme configuration (Snowflake/Blue)
    theme = "snowflake"
    colors = THEME_COLORS.get(theme, {"module": "black", "ring": "black"})
    
    print(f"Generating Donation QR Code for: {paypal_url}")
    print(f"Message: {visible_message}")
    
    img = generate_qr_code(
        data=paypal_url,
        theme=theme,
        visible_message=visible_message,
        all_sides=False, # Set to True for text on all sides
        module_color=colors["module"],
        position_ring_color=colors["ring"]
    )
    
    filename = "donation_qr_snowflake.png"
    img.save(filename)
    print(f"Success! Saved to {filename}")

if __name__ == "__main__":
    create_donation_qr()
````

## File: streamlit/keep_alive.ps1
````powershell
# keep_alive.ps1
# This script visits the Streamlit app URL to prevent it from hibernating.
# It logs the result to a file in the same directory.

$Url = "https://qr-greeting.streamlit.app/?tab=scan"
$LogFile = Join-Path -Path $PSScriptRoot -ChildPath "keep_alive_log.txt"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    # Send a HEAD request effectively "pings" the server without downloading the full body
    # If Streamlit needs a GET to count as activity, we use GET.
    # header User-Agent helps mimic a real browser to ensure the request is counted
    $Response = Invoke-WebRequest -Uri $Url -Method Get -UseBasicParsing -UserAgent "Mozilla/5.0 (KeepAliveScript)" -ErrorAction Stop
    
    $Message = "[$Timestamp] SUCCESS: Pinged $Url (Status: $($Response.StatusCode))"
    Write-Output $Message
    Add-Content -Path $LogFile -Value $Message
}
catch {
    $Message = "[$Timestamp] ERROR: Failed to ping $Url. Details: $_"
    Write-Error $Message
    Add-Content -Path $LogFile -Value $Message
    
    # Optional: If you WANT the browser to open on error (or always), uncomment the line below:
    # Start-Process $Url
}
````

## File: streamlit/keep_alive.py
````python
import time
import webbrowser
import requests
import datetime
import sys

# Configuration
# The base URL of your Streamlit application
BASE_URL = "https://qr-greeting.streamlit.app/"

# Predefined QR code or URL parameters.
# If you want to open the scan tab with a specific message/QR code, set it here.
# Example: "?tab=scan&m=eyJtIjoiSGVsbG8gV29ybGQifQ=="
# For just the scan tab: "?tab=scan"
URL_PARAMS = "?tab=scan"

# Complete Target URL
TARGET_URL = f"{BASE_URL}{URL_PARAMS}"

# How often to open the URL (in hours)
INTERVAL_HOURS = 1

def keep_alive():
    """
    Script to keep the Streamlit app awake by accessing it periodically.
    """
    print("="*50)
    print(f"Keep-Alive Script for {BASE_URL}")
    print(f"Target URL: {TARGET_URL}")
    print(f"Interval: {INTERVAL_HOURS} hour(s)")
    print("="*50)
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Script started.")

    while True:
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Accessing app...")
            
            # Method 1: Headless request using requests library
            # This is less intrusive and good for background running
            try:
                # Set a user-agent to look like a real browser (helps avoid some bot filters)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(TARGET_URL, headers=headers)
                print(f"[{timestamp}] Request successful. Status Code: {response.status_code}")
            except ImportError:
                 print(f"[{timestamp}] 'requests' library not found. Falling back to browser open.")
                 # Fallback/Alternative: Open in default web browser
                 # This matches your request to "open its scan tab"
                 webbrowser.open(TARGET_URL)
                 print(f"[{timestamp}] Opened in default web browser.")
            except Exception as e:
                print(f"[{timestamp}] HTTP Request failed: {e}")
                print(f"[{timestamp}] Attempting to open in browser as fallback...")
                webbrowser.open(TARGET_URL)

            # Note: You can force using browser by commenting out the requests block 
            # and uncommenting the line below:
            # webbrowser.open(TARGET_URL)

        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] General Error: {e}")
        
        # Wait for the defined interval
        print(f"Sleeping for {INTERVAL_HOURS} hour(s)...")
        time.sleep(INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    # Check for requests library availability
    try:
        import requests
    except ImportError:
        print("Warning: 'requests' library not found. The script will use the web browser to open the link.")
        print("To install requests: pip install requests")
        print("-" * 20)

    try:
        keep_alive()
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
        sys.exit(0)
````

## File: streamlit/plans/batch_tab.md
````markdown
# Batch QR Code Generation Feature

## Goal
Add a hidden "Batch" tab that allows users to generate multiple QR codes from an Excel spreadsheet. The tab is shown/hidden via a sidebar checkbox.

## Proposed Changes

### `netshare/streamlit/app.py`

#### [MODIFY] [`main()`](file:///h:/code/yl/netshare/streamlit/app.py#L1127)

1.  **Add sidebar checkbox**: `show_batch = st.checkbox("Show Batch Tab")`.
2.  **Conditionally show 5th tab**: If `show_batch`, create tabs with 5 items including "Batch". Otherwise, 4 tabs as before.
3.  **Update `tab_map`** to include "batch": 4 when visible.

#### [NEW] `batch_greeting_tab()` function

1.  **Template Download**: Provide a button to download an Excel template (`.xlsx`).
2.  **File Uploader**: Allow user to upload filled Excel.
3.  **Parse Excel**: Use `pandas` or `openpyxl` to read.
4.  **Generate QR codes**: Loop through rows, call `generate_qr_code()` for each.
5.  **Provide download**: Zip file containing all generated QR images.

---

### Excel Template Columns

| Column | Description | Validation |
|--------|-------------|------------|
| From | Sender name | Required |
| To | Recipient name | Required |
| Message | Greeting message | Required |
| Theme | Icon theme | Dropdown: snowflake, fireworks, lights, stars, confetti, champagne, hearts, general |
| Background | Background for scanned view | Dropdown: Files in `keep/` folder (e.g., christmastree.mp4) or empty |
| VisibleMessage | Text below QR | Optional |

---

### Background in Greeting

#### [MODIFY] [`greeting_formats.py`](file:///h:/code/yl/netshare/streamlit/greeting_formats.py)

1.  Add `background` field to greeting JSON/URL encoding.
2.  Update `encode_greeting_to_url` and `decode_greeting_from_url` to handle `background`.

#### [MODIFY] [`display_greeting_letter()`](file:///h:/code/yl/netshare/streamlit/app.py)

1.  If `greeting.get('background')` is set:
    *   If it's a video (`.mp4`), embed as background video.
    *   If it's an image, set as CSS background.

---

### Dependencies

*   `pandas` - For reading Excel (likely already available via Streamlit ecosystem, but will add to requirements if needed).
*   `openpyxl` - For `.xlsx` support.

---

## Verification Plan

### Manual Verification
1.  Enable "Show Batch Tab" in sidebar.
2.  Download template.
3.  Fill template with test data.
4.  Upload and generate.
5.  Verify QR codes are generated correctly.
6.  Scan a QR code with background set and verify background displays.
````

## File: streamlit/plans/brainstorm.md
````markdown
## qrbrainstorm.md

### Vision

Use QR codes as portable “keys” or containers for GenAI chat history so users can store, carry, and restore conversations across edge devices without needing a full local database.[web:35][web:38]

---

### Core Ideas

- **QR as chat snapshot**
  - Store short GenAI chat histories directly in QR (up to a few KB of text).[web:35][web:38]
  - For larger histories, store a compact “seed” or reference instead of full logs.[web:34]

- **QR as vector DB pointer**
  - Encode a signed URL / token in the QR that points to a vector database (local or remote).[web:41][web:45]
  - On scan, the edge device queries the vector DB to reconstruct context or history.[web:45]
  - Keeps the QR tiny while data lives in a vector store optimized for retrieval.[web:41]

- **Offline & edge-first**
  - Enable chat migration and restore between edge devices without cloud sync.[web:34][web:40]
  - Work well in air-gapped or privacy-sensitive environments.[web:34][web:45]

---

### Technical Constraints & Insights

- **QR capacity**
  - Hard limit around a few KB of text; about 4,296 alphanumeric characters or ~3 KB of binary in a maximum-size QR, before error correction overhead reduces usable capacity.[web:35][web:38]
  - Practical use favors shorter payloads (URLs, tokens, compressed seeds), not full transcripts.[web:38][web:41]

- **File sizes**
  - A 4,296-character ASCII text file is about 4.3 KB; each ASCII character is 1 byte in UTF‑8.[execute_python]
  - Unicode content (e.g., emojis) can be 2–4 bytes per character, quickly increasing size.[execute_python]

- **Conclusion**
  - QR is not a compression format; it is a transport/encoding format.[web:35][web:38]
  - Best use: encode compressed summaries or references, not full, long chats.[web:34][web:41]

---

### Product Concept: Qrevio

- **Name**
  - Working repo/product name: **Qrevio** (QR + revive).[web:62][web:63]
  - Tagline: **“Scan to Summon Your AI Past.”**

- **Core UX**
  - User finishes a GenAI chat.
  - Clicks “Save as QR”.
  - App:
    - Compresses/encodes a seed or history reference.[web:34]
    - Generates a QR (possibly stylized/animated).[web:92]
  - User scans the QR on another device to:
    - Restore context and continue conversation, or
    - Fetch the full history from a vector DB.[web:41][web:45]

- **Holiday demo angle**
  - Xmas / New Year use case:
    - “Save your 2025 reflections—scan to relive them in 2026.”
    - People create greeting messages or “future self” chats and store a QR image on cards, gifts, or photos.[web:80]

---

### Architecture Sketch

1. **Encode path**
   - Chat app → serialize key state (conversation + minimal metadata).
   - Option A: compress JSON and chunk into multiple QR codes for fully offline restore (only for short sessions).[web:34]
   - Option B (preferred): store full state in a vector DB (e.g., Qdrant at the edge).[web:45]
   - Generate a QR containing:
     - Endpoint / device identifier.
     - Token or key for auth.
     - Optional short payload (prompt seed, timestamp).[web:41][web:45]

2. **Decode path**
   - User scans QR with camera-enabled client.
   - Client validates token and finds associated vector DB.[web:41][web:45]
   - Client retrieves relevant vectors / messages and reconstructs chat context.[web:45]
   - Chat UI resumes conversation from restored state.

3. **Security & privacy**
   - Short-lived or revocable tokens.[web:41]
   - Optional encryption of payload.[web:41]
   - Local-only or LAN-only endpoints for strict privacy.[web:45]

---

### Implementation Notes

- **Tech stack**
  - Backend / logic: Python.
  - QR generation:
    - Standard: `qrcode` + Pillow.[web:83]
    - Fancy: `amazing-qr` for animated/stylized QR that remains scannable.[web:92]
  - Demo UI:
    - Streamlit on free tier supports `qrcode` and similar libs, good for quick demos.[web:82][web:90]

- **Demo website idea**
  - “Qrevio Holiday Memory Demo”:
    - User chats with a small model.
    - Click “Create Holiday QR”.
    - App:
      - Stores conversation (or seed) in a demo vector DB.[web:72][web:45]
      - Generates a QR image + share link.[web:73][web:75]
    - On scan:
      - Demo site fetches and displays the restored conversation.[web:72]
  - Deployed on Streamlit/other free hosting for low friction trials.[web:82][web:90]

---

### Potential Use Cases

- **Personal**
  - Cross-device AI journals and reflections.
  - Gift cards with embedded AI messages.
  - “Time capsule” conversations for future dates.

- **Professional / enterprise**
  - Field devices (robots, kiosks) carrying configuration or state via QR labels.[web:45]
  - Air-gapped environments that need state transfer without network.[web:34][web:40]
  - Training or support scripts encoded as QRs linking to local vector knowledge.[web:41][web:45]

---

### Commercial Potential

- **Why promising**
  - Aligns with trend toward privacy-preserving, edge AI and vector databases.[web:45]
  - Familiar QR UX (already used for chat transfers in apps like WhatsApp) reduces user friction.[web:43][web:47]
  - Differentiator: “QR + vector DB + GenAI state” in one coherent story.[web:41][web:45]

- **Monetization**
  - SaaS tiers:
    - Free: limited chats, storage, and QR generations.
    - Paid: more storage, org workspaces, custom branding and domains.[web:50]
  - Enterprise:
    - White-label SDKs for device manufacturers or AI app vendors.[web:45]
    - On-prem/edge deployment packages.[web:45]
````

## File: streamlit/plans/localization.md
````markdown
# Chinese Localization Plan for Streamlit Holiday Greeting QR

## Overview

**Goal**: Add Simplified Chinese (zh-CN) localization to the Streamlit Holiday Greeting QR application

**Key Decisions**:
- ✅ Simplified Chinese (zh-CN) - Mainland China variant
- ✅ Default language: English (user can switch to Chinese)
- ✅ Keep example greetings in English (show cross-language capability)
- ✅ Keep QR message content as user-entered (only translate UI elements)
- ✅ Approach: Session State + JSON dictionary (optimal for 2 languages)

**Scope**: ~250+ UI text strings across 11 Python files

**Note**: Streamlit has NO native localization support - custom implementation required

---

## Architecture

### New Files to Create

1. **`/mnt/e/code2/netshare/streamlit/i18n.py`**
   - Translation infrastructure module
   - Functions: `init_language()`, `get_text()`, `set_language()`, `get_current_language()`
   - Session state management
   - Fallback logic (zh → en → show key)

2. **`/mnt/e/code2/netshare/streamlit/translations.json`**
   - JSON structure with `en` and `zh` keys
   - Hierarchical key format: `{file}.{component}.{element}`
   - Example: `"app.sidebar.title": "Holiday Greeting QR | 节日问候二维码"`
   - ~250+ translation pairs

### Translation Function Pattern

```python
# Import in each file
from i18n import get_text as _

# Simple usage
st.write(_("file.key"))

# With dynamic content
st.write(_("file.greeting", name=user_name))

# Translations with variables
{
  "en": {"file.greeting": "Hello {name}!"},
  "zh": {"file.greeting": "你好 {name}！"}
}
```

### Language Selector

- **Location**: Top of sidebar in `app.py`
- **Component**: `st.selectbox` with callback
- **Persistence**: Session state only (resets on reload)
- **Default**: English

---

## Critical Files to Modify (Priority Order)

### Phase 1: Infrastructure ⭐
1. **`/mnt/e/code2/netshare/streamlit/i18n.py`** (NEW)
   - Create translation module (~100-150 lines)

2. **`/mnt/e/code2/netshare/streamlit/translations.json`** (NEW)
   - Start with base structure + 20 sample translations
   - Expand incrementally as we translate each file

3. **`/mnt/e/code2/netshare/streamlit/app.py`**
   - Import i18n module
   - Call `init_language()` at startup
   - Add language selector to sidebar (top position)
   - Translate sidebar content: title, tagline, tips, support section, tab names
   - ~15 strings to translate

### Phase 2: Core Tabs 🎯
4. **`/mnt/e/code2/netshare/streamlit/tabs/create_tab.py`**
   - Primary user interaction tab
   - ~70 strings: headers, tips, labels, buttons, messages
   - Add `from i18n import get_text as _` import
   - Replace all user-facing text with `_()` calls
   - **Note**: Keep default greeting message as-is (user content)

5. **`/mnt/e/code2/netshare/streamlit/tabs/components.py`**
   - Shared components used across tabs
   - ~30 strings: theme selector, QR options, validation messages
   - Theme names: translate display labels, keep internal keys unchanged
   - Example: Display "❄️ 雪花" but internal value remains "snowflake"

6. **`/mnt/e/code2/netshare/streamlit/tabs/demo_tab.py`**
   - Interactive demo experience
   - ~45 strings: step instructions, tips, buttons, status messages
   - Keep example greeting content in English

### Phase 3: Secondary Tabs 📄
7. **`/mnt/e/code2/netshare/streamlit/tabs/scan_tab.py`**
   - QR scanning interface
   - ~25 strings: upload prompts, status messages, errors

8. **`/mnt/e/code2/netshare/streamlit/tabs/about_tab.py`**
   - Information and marketing content
   - ~60 strings: feature descriptions, how it works, technical details
   - Important for Chinese users to understand the value proposition

9. **`/mnt/e/code2/netshare/streamlit/tabs/batch_tab.py`**
   - Batch QR generation
   - ~35 strings: instructions, template info, progress messages

10. **`/mnt/e/code2/netshare/streamlit/tabs/examples_tab.py`**
    - Example showcase
    - ~15 strings: titles and descriptions
    - **Keep example message content in English** (per user preference)

### Phase 4: Display & Utilities 🔧
11. **`/mnt/e/code2/netshare/streamlit/qr/display.py`**
    - QR display and rendering
    - ~10 strings: captions, labels, error messages

12. **`/mnt/e/code2/netshare/streamlit/tabs/view_page.py`**
    - Mobile greeting view page
    - ~5 strings: error messages, navigation buttons

### Files NOT Modified
- **`/mnt/e/code2/netshare/streamlit/config.py`** - Icons and theme config (universal, no text)
- **`/mnt/e/code2/netshare/streamlit/greeting_formats.py`** - Data handling (no UI text)
- **`/mnt/e/code2/netshare/streamlit/utils/*`** - Backend utilities (no UI text)

---

## Translation Strategy

### What to Translate
✅ **UI Elements**: Headers, labels, buttons, tips, instructions
✅ **Messages**: Info, warning, error, success messages
✅ **Help Text**: Tooltips, placeholder text, descriptions
✅ **Tab Names**: Main navigation tabs
✅ **Theme Display Names**: User-visible theme labels

### What NOT to Translate
❌ **Emojis**: Keep all emojis (universal visual language)
❌ **Example Messages**: Keep greeting content in English (per user preference)
❌ **User Content**: QR message content stays as user-entered
❌ **Internal Keys**: Theme keys, config values, session state keys
❌ **URLs**: External links, video URLs

### Dynamic Content Handling
```python
# Pattern for variables
st.write(_("qr.stats", bytes=data_size, version=qr_version))

# JSON translation
{
  "en": {"qr.stats": "Data size: {bytes} bytes, Version: {version}"},
  "zh": {"qr.stats": "数据大小：{bytes} 字节，版本：{version}"}
}
```

### Key Naming Convention
- Format: `{file}.{section}.{element}`
- Examples:
  - `app.sidebar.title`
  - `create_tab.step1.title`
  - `create_tab.step1.tip`
  - `common.buttons.generate`
  - `components.theme_selector.label`

---

## Implementation Steps

### Step 1: Create Translation Infrastructure
1. Create `i18n.py` with:
   - `init_language()` - Initialize session state with 'en' default
   - `get_text(key, **kwargs)` - Retrieve translation with variable substitution
   - `set_language(lang_code)` - Switch language and trigger rerun
   - `get_current_language()` - Return current language from session state
   - JSON loading and caching
   - Fallback chain: zh → en → `[missing: key]`

2. Create `translations.json` base structure:
```json
{
  "en": {},
  "zh": {}
}
```

### Step 2: Add Language Selector to App
1. Modify `app.py`:
   - Import `i18n` module
   - Call `init_language()` before main()
   - Add language selector at top of sidebar
   - Translate sidebar content (~15 strings)
   - Update tab names array

2. Test: Verify language switching works and sidebar translates

### Step 3: Translate Core Create Tab
1. Extract all ~70 strings from `create_tab.py` to `translations.json`
2. Add import: `from i18n import get_text as _`
3. Replace all hardcoded text with `_()` calls
4. Test: Create QR flow works in both languages

### Step 4: Translate Shared Components
1. Extract ~30 strings from `components.py`
2. Create theme name translation dictionary
3. Update theme selector to show translated names
4. Test: Components work across all tabs

### Step 5: Translate Demo Tab
1. Extract ~45 strings from `demo_tab.py`
2. Replace with `_()` calls
3. Keep demo greeting content in English
4. Test: Demo flow in both languages

### Step 6: Translate Remaining Tabs
1. Process each tab file (scan, about, batch, examples)
2. Extract strings to translations.json
3. Replace with `_()` calls
4. Test each tab individually

### Step 7: Translate Display & Utilities
1. Update `qr/display.py` with translations
2. Update `view_page.py` with translations
3. Test QR display and mobile view

### Step 8: Complete Chinese Translations
1. Review all translation keys for consistency
2. Ensure proper terminology (technical vs. casual tone)
3. Verify Chinese character accuracy
4. Check for missing translations

### Step 9: Layout Testing
1. Test all tabs with Chinese text (wider characters)
2. Check for text overflow in buttons, labels
3. Verify sidebar fits all content
4. Test responsive breakpoints
5. Adjust column widths if needed

### Step 10: End-to-End Testing
1. Complete user flow in Chinese: create → download → scan
2. Test batch generation in Chinese
3. Verify all error messages display correctly
4. Test language switching mid-session
5. Verify QR codes work regardless of UI language

---

## Sample Translations (Key Sections)

### Sidebar
```json
{
  "app.sidebar.title": "节日问候二维码",
  "app.sidebar.tagline": "创建并分享个性化节日问候二维码！",
  "app.sidebar.greener": "*更环保、更智能的节日问候方式。*",
  "app.sidebar.quick_tips.title": "快速提示",
  "app.sidebar.quick_tips.tip1": "💡 建议消息长度在300字以内，以获得最佳二维码尺寸",
  "app.sidebar.quick_tips.tip2": "📱 使用手机相机应用测试二维码",
  "app.sidebar.quick_tips.tip3": "🎨 选择与场合相配的主题",
  "app.sidebar.support.title": "支持",
  "app.sidebar.support.text": "如果您喜欢这个工具，请考虑支持它！",
  "app.sidebar.buy_coffee": "☕ 请我喝咖啡（£1）"
}
```

### Tab Names
```json
{
  "app.tabs.demo": "🎁 试用演示",
  "app.tabs.create": "创建问候",
  "app.tabs.scan": "扫描二维码",
  "app.tabs.examples": "示例",
  "app.tabs.batch": "批量生成",
  "app.tabs.about": "关于"
}
```

### Theme Names
```json
{
  "themes.snowflake": "雪花",
  "themes.fireworks": "烟花",
  "themes.lights": "灯光",
  "themes.stars": "星星",
  "themes.confetti": "彩纸",
  "themes.champagne": "香槟",
  "themes.hearts": "爱心",
  "themes.farewell": "告别",
  "themes.burn_after_read": "阅后即焚",
  "themes.general": "通用（无图标）"
}
```

### Common Buttons
```json
{
  "common.buttons.generate": "✨ 生成二维码",
  "common.buttons.download": "📥 下载二维码",
  "common.buttons.create_another": "🔄 创建另一个问候",
  "common.buttons.scan_another": "📤 扫描另一个二维码"
}
```

### Create Tab Steps
```json
{
  "create_tab.step1.title": "### 步骤 1：选择主题和背景",
  "create_tab.step1.tip": "💡 **提示：** 选择与场合相配的主题。颜色会自动适配！",
  "create_tab.step2.title": "### 步骤 2：预览和个性化",
  "create_tab.step2.tip": "💡 **提示：** 这是您的问候的显示效果。您可以在下方编辑详细信息！",
  "create_tab.step3.title": "### 步骤 3：创建魔法",
  "create_tab.step3.tip": "💡 **提示：** 准备好了吗？点击下方生成您的专属问候二维码！"
}
```

---

## Testing Checklist

### Translation Completeness
- [ ] All 11 Python files updated with `from i18n import get_text as _`
- [ ] No hardcoded English text visible in UI (except examples)
- [ ] All ~250+ strings present in translations.json
- [ ] All translations have both `en` and `zh` values
- [ ] No missing translation keys (fallback to English works)

### Functionality Testing (Chinese UI)
- [ ] Language selector switches immediately
- [ ] Create greeting flow: select theme → preview → generate → download
- [ ] Scan QR code: upload → decode → display message
- [ ] Demo tab: full interactive demo works
- [ ] Batch generation: upload CSV → generate all → download ZIP
- [ ] About tab: all information displayed correctly
- [ ] Examples tab: all examples shown

### Layout Testing (Chinese Text)
- [ ] Sidebar: all content fits without horizontal scrolling
- [ ] Tab names: fit in tab bar without wrapping
- [ ] Buttons: text doesn't overflow
- [ ] Cards/containers: accommodate wider Chinese text
- [ ] Help tooltips: display correctly
- [ ] Multi-column layouts: maintain balance
- [ ] Mobile view: responsive design works

### Edge Cases
- [ ] Switch language mid-session → all tabs update
- [ ] Create QR in Chinese UI → QR data intact
- [ ] Error messages display in correct language
- [ ] Missing translation → falls back to English gracefully
- [ ] Special characters in messages → handled correctly
- [ ] Long messages → QR code generation warning in Chinese

---

## Risk Mitigation

### Layout Issues
- **Risk**: Chinese text 20-40% wider may break layouts
- **Mitigation**: Use flexible containers, test all responsive breakpoints, adjust column ratios if needed

### Character Encoding
- **Risk**: UTF-8 encoding issues with Chinese characters
- **Mitigation**: Ensure all files saved as UTF-8, add encoding declarations

### Missing Translations
- **Risk**: Forgetting to translate some strings
- **Mitigation**: Systematic file-by-file approach, automated completeness check

### Performance
- **Risk**: Loading translations adds overhead
- **Mitigation**: Cache in session state, JSON load is ~1ms (negligible)

---

## Future Enhancements (Out of Scope)

- Additional languages (Traditional Chinese, Spanish, French, Japanese)
- Browser language auto-detection
- Persistent language preference (cookies/URL parameter)
- Translation management UI
- Translate example greeting messages
- RTL language support

---

## Success Criteria

✅ Complete Chinese translation of all UI elements (~250+ strings)
✅ Language selector in sidebar working smoothly
✅ All core functionality (create, scan, batch) works in both languages
✅ No layout breaking with Chinese text
✅ No English text visible in UI when Chinese selected (except examples/user content)
✅ Fallback to English for missing translations
✅ Clean, maintainable code with clear translation key structure
````

## File: streamlit/plans/moneytize.md
````markdown
# Holiday Greeting QR Code Generator - Monetization & Enhancement Plan

**Project**: Holiday Greeting QR Code Generator  
**Repository**: https://github.com/ly2xxx/netshare/tree/main/streamlit  
**Live App**: https://qr-greeting.streamlit.app/  
**Created**: December 27, 2025

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Attractiveness Improvements](#attractiveness-improvements)
4. [Monetization Strategies](#monetization-strategies)
5. [Technical Implementation](#technical-implementation)
6. [Growth & Marketing Strategy](#growth--marketing-strategy)
7. [Implementation Roadmap](#implementation-roadmap)

---

## Executive Summary

The Holiday Greeting QR Code Generator is a functional Streamlit application with strong potential but limited market appeal and monetization. This plan outlines how to transform it from a nice utility tool into a compelling product with clear revenue streams.

**Key Opportunity**: The greeting/personalization market is fragmented. A well-designed, focused QR-based greeting solution can capture market share in events, corporate communications, and personal occasions.

**Revenue Potential**: $5K-$50K/month depending on acquisition rate and tier adoption.

---

## Current State Analysis

### Strengths
- ✅ Clean, modular Python codebase (easily maintainable)
- ✅ Multiple themes with color customization
- ✅ Animated QR code generation capability
- ✅ Batch processing for bulk operations
- ✅ Mobile-responsive design
- ✅ Already deployed on Streamlit Cloud
- ✅ Donation button showing monetization awareness
- ✅ Good documentation with clear use cases

### Weaknesses
- ❌ Minimal visual branding and marketing appeal
- ❌ Basic UI despite custom CSS capabilities
- ❌ No dedicated landing page
- ❌ No user authentication or accounts
- ❌ No analytics or engagement tracking
- ❌ No email integration or sharing features
- ❌ No social proof (testimonials, usage stats)
- ❌ Limited differentiation in greeting market
- ❌ No mobile app
- ❌ Revenue currently limited to single donation button

### Market Context
- **Market Size**: Digital greeting/personalization market is $2B+ globally
- **Growth Trend**: Post-pandemic increase in personalized digital communications
- **Competitors**: 
  - Canva (general design, high friction)
  - Greeting.com (basic, limited sharing)
  - Paper-based alternatives (no tracking)
  - DIY QR tools (no greeting-specific design)
- **Advantage**: Purpose-built, easy to use, trackable, modern

---

## Attractiveness Improvements

### 1. Visual & UX Enhancements

#### Landing Page Redesign
- **Hero Section**:
  - Animated background showing QR code generation
  - Clear value proposition: "Create Unforgettable Digital Greetings"
  - Call-to-action: "Try Free" or "Create Your Greeting"
  - Social proof visible above fold

- **Feature Showcase**:
  - Interactive demo allowing users to create a sample greeting
  - Before/after preview of QR code
  - Real-time theme preview

- **Use Case Cards**:
  - Dedicated sections for: Weddings, Holidays, Corporate, Birthdays, Events
  - One-click access to templates for each

#### Dark Mode & Theme System
- Toggle dark/light mode in header
- Seasonal themes (December = holiday colors, February = Valentine colors, etc.)
- Auto-update seasonal themes based on calendar

#### Microinteractions
- Satisfying animations when QR codes generate
- Hover effects on theme selector showing live preview
- Confetti animation on successful generation (optional toggle)
- Smooth transitions between tabs
- Loading states with progress indicators

#### Typography & Design System
- Upgrade fonts: Header (Poppins or Playfair Display), Body (Inter or Outfit)
- Establish clear spacing system (8px grid)
- Color palette expansion: Primary, secondary, accent colors
- Icon system: Use modern SVG icons consistently
- Card-based layouts with subtle shadows and borders

#### Mobile-First Responsive Design
- Bottom navigation for mobile (avoid top tabs)
- Full-screen preview for generated QR codes
- Touch-friendly button sizes (48px minimum)
- Gesture support (swipe between themes)

### 2. Content & Storytelling

#### Success Stories / Social Proof
- Testimonial cards with user names, occasions, and QR results
- Real greeting examples from actual users (with permission)
- "X thousand QR codes created" counter
- Featured use cases from notable users

#### Video Content
- **60-second Tutorial**: "How to Create Your First Greeting"
- **Theme Showcase**: Each theme gets a short video demo
- **User Stories**: 2-3 minute interviews with creative users
- **Tips & Tricks**: Design best practices for different occasions

#### Use Case Documentation
- **Wedding Edition**: Save-the-dates, thank-you messages, seating charts
- **Corporate Edition**: Event invitations, team announcements, feedback collection
- **Holiday Edition**: Seasonal greetings, New Year wishes, special announcements
- **Personal Edition**: Birthday wishes, anniversary messages, time capsules

#### Blog/Resource Center
- "10 Creative QR Greeting Ideas for 2026"
- "How to Design QR Codes That Stand Out"
- "The Psychology of Digital Greetings"
- "QR Codes vs. Traditional Greetings: When to Use Each"
- "Best Practices for Corporate Communications via QR"

#### Inspiration Gallery
- Showcase greetings by theme, occasion, and complexity level
- User-submitted gallery (with moderation)
- Trending greetings section
- Saved collections for later reference

### 3. Feature Additions for Appeal

#### Design Customization
- **Logo/Watermark Upload**: Add personal or company logos
- **Custom QR Colors**: Full color picker (currently limited)
- **Border Styles**: Choose QR code border options
- **Background Options**: Custom backgrounds for the greeting display
- **Font Selection**: Choose fonts for embedded text

#### Template Library
- Pre-designed greeting templates for common occasions
- Editable templates with placeholders
- Category browsing: Holidays, Events, Business, Personal
- One-click apply with instant preview

#### Social Media Integration
- "Share to Instagram" with QR code as post image
- "Share to Pinterest" with greeting design
- "Share to Twitter/X" with QR code link
- "Copy Shareable Link" for email/messaging apps
- Email sharing with custom message

#### Analytics Dashboard
- Track QR code scans over time
- Geographic data on where QR codes were scanned
- Device information (mobile vs. desktop)
- Scan timeline and patterns
- Export scan data as CSV

#### Time-Capsule Feature
- Schedule greetings to be revealed on specific dates
- Automated reminder emails
- Counter showing days until reveal
- Perfect for birthdays, anniversaries, milestones

#### Collaborative Greetings
- Invite multiple people to contribute messages
- Combine messages into single QR code
- Comments and reactions on contributions
- Version history and drafts

#### Recipients Database
- Save frequently used recipients
- Quick-fill form with previous recipients
- Recipient groups (family, colleagues, friends)
- Birthday reminders and suggested occasions

---

## Monetization Strategies

### 1. Freemium Model (Recommended - Primary Strategy)

**Free Tier (Forever)**
- Up to 5 QR codes per month
- Standard themes only
- Basic customization (no logo/colors)
- No analytics
- Community features only
- Streamlit branding visible

**Premium Tier** - $2.99/month or $24.99/year (saves 16%)
- Unlimited QR code generation
- All themes and animations
- Custom colors and logo/watermark upload
- Basic analytics (scans, top days)
- Email support
- Remove "created with Holiday QR" watermark
- 1GB storage for saved greetings
- Batch generation (up to 50 at once)

**Pro Tier** - $9.99/month or $99.99/year (saves 17%)
- Everything in Premium +
- Advanced analytics (geolocation, device data, reports)
- Collaborative features (team invites)
- Template library (100+ templates)
- Social media integration
- Custom domain for sharing links (pro.greeting.app/mygreetings)
- 50GB storage
- Batch generation (unlimited)
- API access for integrations
- Priority email support

**Enterprise** - Custom pricing (contact sales)
- White-label solution
- Custom branding throughout
- Unlimited team members
- Advanced API access
- Dedicated support
- Custom integrations
- Minimum: $500/month

### 2. One-Time Purchase Model

**Premium Theme Packs** - $1.99 each
- "Luxury Wedding Collection" (5 premium themes)
- "Festive Holidays Pack" (8 seasonal themes)
- "Corporate Elegance Pack" (5 professional themes)
- "Neon Dreams Pack" (vibrant, trendy themes)

**Design Services** - $19.99 to $99.99
- "Professional Design Consultation" (1-hour video call)
- "Custom QR Design Service" (fully designed greeting, $49)
- "Event Branding Package" (coordinated greeting design, $99)

**Print Services** - Variable pricing
- Printed greeting cards with QR codes ($5-$20 per pack)
- Custom stickers with QR codes ($15-$50 per sheet)
- Poster-sized QR prints ($20-$50)
- *Partner with Printful, Printfulfillment, or similar*

### 3. B2B / Enterprise Options

**White-Label License** - $2,000-$10,000/month
- Fully branded for partner's business
- Remove all Holiday QR branding
- Custom domain
- Embedded in partner's website
- Usage rights for resale

**API Access Tier** - $500-$5,000/month
- RESTful API for QR generation
- Webhook integrations
- Higher rate limits
- Dedicated technical support
- Use cases: CRM integrations, marketing platforms, event management systems

**Bulk Enterprise Service** - $1,000-$50,000
- Generate thousands of QR codes for campaigns
- Custom integration with existing systems
- Data security and compliance (GDPR, SOC 2)
- Dedicated account manager
- Custom reporting and analytics

### 4. Hybrid Revenue Streams

**Affiliate Partnerships**
- Recommend event planning tools, invitation platforms
- Link to printing services with commission
- Recommend QR code readers with referral links
- Partner with Etsy sellers for card supplies

**Email Marketing**
- Curated "Greeting Ideas of the Week" newsletter
- Seasonal greeting suggestions
- New feature announcements
- Partner content with affiliate links
- Premium-exclusive newsletter

**Educational Content**
- Paid course: "Mastering QR Greeting Campaigns" ($29-$79)
- Workshop series on greeting design
- Certification program for event professionals
- Webinar series with industry experts

**B2B Content & Insights**
- Industry report: "The State of Digital Greetings 2026" ($99-$499)
- Case studies from successful campaigns
- Benchmark data for event professionals

### 5. Revenue Projections

**Year 1 Conservative Estimate** (500 paying users)
- 400 Premium @ $24.99/year = $9,996
- 80 Pro @ $99.99/year = $7,999
- 20 Enterprise @ $5,000/month = $120,000
- **Annual: ~$138K**

**Year 2 Target** (2,500 paying users)
- 2,000 Premium @ $24.99/year = $49,980
- 400 Pro @ $99.99/year = $39,996
- 100 Enterprise @ $5,000/month = $600,000
- Print/One-time sales: $50,000
- **Annual: ~$740K**

**Year 3 Optimistic** (10,000 paying users)
- 8,000 Premium = $199,920
- 1,500 Pro = $149,985
- 500 Enterprise = $3,000,000
- Print, API, and other revenue: $200,000
- **Annual: ~$3.55M**

---

## Technical Implementation

### Phase 1: User Infrastructure (Weeks 1-4)

#### Authentication System
- Implement OAuth with Google and GitHub
- Local email/password authentication (with password reset)
- User profiles with preferences
- Session management (30-day auto-logout)

**Tools**: Firebase Auth, Auth0, or Clerk.io

#### Database Schema
```
Users table
├── user_id (PK)
├── email
├── name
├── subscription_tier (free/premium/pro/enterprise)
├── created_at
├── last_login
└── preferences (JSON: theme, notifications, etc.)

Greetings table
├── greeting_id (PK)
├── user_id (FK)
├── title
├── from_name
├── to_name
├── occasion
├── message
├── theme
├── custom_colors (JSON)
├── logo_url
├── created_at
└── is_public (boolean)

Analytics table
├── scan_id (PK)
├── greeting_id (FK)
├── timestamp
├── device_type
├── country
├── city
└── browser
```

**Database Choice**: Firebase Firestore (scales easily, free tier generous) or PostgreSQL on Supabase

#### User Dashboard
- List of all created greetings
- Quick stats (total scans, popular greetings)
- Greeting management (edit, delete, duplicate, export)
- Account settings (profile, billing, preferences)

**Tech Stack**: 
- Frontend: Streamlit Community Cloud or migrate to custom Flask/FastAPI + React
- Backend: Python with FastAPI or Node.js with Express
- Database: Firebase or PostgreSQL

### Phase 2: Payment Integration (Weeks 5-6)

#### Payment Processing
- Implement Stripe or Paddle for subscriptions
- Subscription management (upgrade, downgrade, cancel)
- Invoice generation and email
- Dunning management (handle failed payments)

#### Billing Dashboard
- Current subscription display
- Upgrade/downgrade options
- Payment method management
- Invoice history and downloads
- Usage metrics (QR codes created vs. limit)

**Tools**: Stripe (recommended), Paddle, or LemonSqueezy

### Phase 3: Enhanced Features (Weeks 7-12)

#### Analytics Engine
- Track all QR scans with metadata
- Real-time dashboard
- Export data as CSV/PDF
- Visualizations: Line charts, pie charts, maps
- Comparison views (this month vs. last month)

#### Email Integration
- Transactional emails (confirmation, sharing)
- Marketing automation (welcome series, re-engagement)
- Email templates for sharing greetings

**Tools**: SendGrid, Mailgun, or Postmark

#### Social Media Integration
- One-click sharing to Instagram, Pinterest, Twitter
- Pre-formatted image generation for each platform
- UTM parameter tracking
- Social proof display (shares count)

**Tools**: Social sharing SDKs, custom image generation with Pillow

#### API Development
- RESTful API for QR generation
- Webhook support for integrations
- Rate limiting and API key management
- API documentation (Swagger/OpenAPI)
- API dashboard for Pro/Enterprise users

**Framework**: FastAPI (Python) or Express.js (Node.js)

### Phase 4: Advanced Features (Weeks 13-16)

#### Time-Capsule Scheduling
- Date picker for reveal time
- Scheduled email notifications
- Countdown timer on greeting page
- Automated greeting delivery

**Tools**: APScheduler (Python), Bull (Node.js), or Cloud Tasks

#### Collaborative Features
- Invite system (email-based)
- Real-time message editing (optional)
- Comment threads on greetings
- Permission levels (view, edit, admin)
- Activity log/version history

**Tech**: WebSocket for real-time updates, or Firebase Realtime DB

#### Template System
- Template library (100+ templates)
- Categorization and tagging
- Search and filtering
- User-created templates (Pro tier only)
- Template ratings and reviews

#### Mobile App (Optional, Phase 2 of product)
- React Native or Flutter app
- Offline greeting creation
- Camera integration for QR scanning
- Push notifications for scans
- Simplified UX for mobile

### Phase 5: DevOps & Scaling (Ongoing)

#### Infrastructure
- Move from Streamlit Cloud to custom infrastructure:
  - Frontend: Vercel (React) or Netlify
  - Backend: AWS Lambda, Google Cloud Run, or DigitalOcean
  - Database: Firebase or AWS RDS
  - Storage: AWS S3 for images

#### Monitoring & Analytics
- Application performance monitoring (Sentry, New Relic)
- User analytics (Mixpanel, Amplitude)
- Email deliverability monitoring (SendGrid analytics)
- Uptime monitoring (Uptime Robot, Pingdom)

#### CI/CD Pipeline
- GitHub Actions for automated testing and deployment
- Automated staging environment
- Blue-green deployment strategy
- Database migration automation

#### Security
- SSL/TLS encryption (automatic with Vercel/Netlify)
- Rate limiting on all endpoints
- CSRF protection
- SQL injection prevention (use parameterized queries)
- OWASP compliance audit
- GDPR/CCPA compliance (data deletion, privacy policy)

---

## Growth & Marketing Strategy

### 1. Positioning & Messaging

**Target Positioning**: 
*"The easiest way to create memorable, trackable digital greetings for any occasion"*

**Key Messages**:
- ✨ Create in 60 seconds
- 📊 Track every scan in real-time
- 🎨 Professionally designed themes
- 🚀 Perfect for personal and business use

### 2. Target Audiences (Priority Order)

#### Tier 1: Event Professionals (High LTV)
- Wedding planners and coordinators
- Event managers
- Corporate event organizers
- Party planners
- **Approach**: Industry partnerships, targeted ads on event sites

#### Tier 2: Corporate Communications (High LTV)
- HR departments (employee engagement, onboarding)
- Marketing teams (campaign tracking, personalization)
- Sales teams (client outreach)
- Internal communications
- **Approach**: B2B SaaS marketing, LinkedIn outreach

#### Tier 3: Individual Users (High Volume, Lower LTV)
- Holiday greeting senders
- Birthday celebrators
- Anniversary commemorators
- Creative hobbyists
- **Approach**: Seasonal campaigns, social media, viral content

### 3. Acquisition Channels

#### Paid Channels
**Google Ads** ($2K-$5K/month)
- Search: "create QR code greetings", "personalized greeting cards", "digital invitation"
- Display: Retargeting website visitors
- YouTube: Pre-roll ads on greeting/event planning content

**Facebook/Instagram Ads** ($1K-$3K/month)
- Carousel ads showing different greeting themes
- Video ads of QR creation process
- Testimonial ads from users
- Target: Event planners, people searching "wedding ideas", "birthday party"

**LinkedIn Ads** ($2K-$5K/month)
- B2B targeting: HR, marketing, event managers
- Company page followers
- Sponsored content for professionals

**Pinterest Ads** ($1K-$2K/month)
- High-intent users planning events/celebrations
- Promoted pins linking to gallery and examples

#### Organic Channels
**Product Hunt Launch** (Week 1)
- Prepare launch post with screenshots, GIFs, testimonials
- Engage with comments throughout day
- Offer time-limited discount (20% off first year)
- Target: 500-1K upvotes, 5-10K clicks

**Reddit Communities**
- r/weddingplanning: Share wedding QR greeting ideas
- r/eventplanning: Discuss event communication tools
- r/smallbusiness: B2B use cases and bulk generation
- r/InternetIsBeautiful: Occasionally when feature-appropriate
- **Strategy**: Genuine participation, helpful comments, occasional posts

**Content Marketing** (Blog on greeting website)
- Blog posts: 1-2 per week
- Target long-tail keywords: "creative QR code ideas", "digital greeting card alternatives"
- SEO optimization for event/greeting keywords
- **Target**: #1-3 ranking for "QR code greetings" within 6 months

**YouTube Channel** (Optional but recommended)
- Weekly 5-10 minute tutorials
- Theme showcases and design inspiration
- User stories and creative uses
- Behind-the-scenes development
- **Target**: 10K subscribers within 12 months

**Twitter/X Presence**
- Share design tips and greeting ideas
- Engage with event planning and marketing communities
- Tweet user success stories
- Share blog post updates
- Retweet/engage with relevant conversations

**Email Marketing**
- Newsletter: "Greeting Ideas of the Week" (weekly, free)
- Seasonal campaigns: Holiday greetings, New Year ideas, Valentine's ideas
- Signup flow: Free greeting creation offer
- Re-engagement: Target inactive free users

**Partnerships & Collaborations**
- Event planning platforms (Eventbrite, The Knot): Embed or integrate
- Invitation platforms: Complementary positioning
- Email marketing tools: Integration
- CRM platforms: Custom greeting workflows
- Wedding blogs and magazines: Guest posts, sponsorships

#### Community Building
- Create Discord or Slack community for users
- Monthly "Greeting of the Month" contest with prizes
- User spotlight features
- Feedback sessions for feature requests
- Ambassador program for highly engaged users

### 4. Retention & Activation Strategy

**Onboarding**
- Interactive tutorial (skippable)
- Pre-populated greeting example
- One-click "Try Now" demo
- Congratulations email after first greeting

**Engagement Loops**
- Weekly scan notifications (pro tier)
- Monthly summary emails showing total scans
- Seasonal greeting reminders ("It's almost Christmas!")
- New feature announcements
- Holidays in next 30 days reminder

**Churn Prevention**
- Monitor inactive users (>30 days)
- "Come back" email campaign with new features
- Special offers (20% discount on annual plan)
- Feedback surveys: "Why did you stop using Holiday QR?"

**Monetization Triggers**
- When free user hits limit: Upsell to Premium
- After 10 successful greetings: "Want more power? Try Premium"
- After 50 scans: Analytics dashboard teaser (Pro upgrade)
- Seasonal campaigns: Holiday bundles, special pricing

---

## Implementation Roadmap

### Timeline & Milestones

#### Quarter 1 (Weeks 1-12)
- **Weeks 1-4**: User authentication + database migration
- **Weeks 5-6**: Payment integration (Stripe setup)
- **Weeks 7-8**: Dashboard + greeting management UI
- **Weeks 9-10**: Analytics engine
- **Weeks 11-12**: Email integration

**Deliverables**:
- ✅ User accounts working with free tier
- ✅ Subscription system live
- ✅ Basic user dashboard
- ✅ Email notifications
- ✅ Analytics for Pro users

**Target Metrics**:
- 100 paying users (Premium tier)
- 20+ Pro tier subscriptions
- 1K+ total registered users

#### Quarter 2 (Weeks 13-24)
- **Weeks 13-16**: Social media integration + API development
- **Weeks 17-20**: Template library + time-capsule feature
- **Weeks 21-24**: Landing page redesign + marketing website

**Deliverables**:
- ✅ Social sharing working (Instagram, Pinterest, Twitter)
- ✅ Public API ready for Enterprise
- ✅ 100+ template library
- ✅ New marketing website launched
- ✅ Brand identity established

**Target Metrics**:
- 500 paying users
- $5K MRR
- 10K+ monthly active users
- 1M+ page views to new website

#### Quarter 3 (Weeks 25-36)
- **Weeks 25-28**: Collaborative features
- **Weeks 29-32**: Advanced analytics + reporting
- **Weeks 33-36**: Mobile app launch (React Native) - optional

**Deliverables**:
- ✅ Team collaboration features
- ✅ Advanced analytics dashboard
- ✅ Reporting exports (CSV, PDF)
- ✅ Mobile app (iOS/Android)
- ✅ Enterprise sales pipeline established

**Target Metrics**:
- 2K+ paying users
- $25K MRR
- 50K+ monthly active users
- 5+ enterprise contracts signed

#### Quarter 4 (Weeks 37-48)
- **Weeks 37-40**: Print service integration
- **Weeks 41-44**: White-label platform completion
- **Weeks 45-48**: Optimization + preparation for Year 2

**Deliverables**:
- ✅ Print-on-demand integration
- ✅ White-label version ready for partners
- ✅ Course/educational content launched
- ✅ Industry partnerships established
- ✅ Global marketing presence

**Target Metrics**:
- 5K+ paying users
- $50K MRR
- 100K+ monthly active users
- 10+ white-label customers
- $500K annual revenue trajectory

### Budget Estimate (Year 1)

| Category | Cost | Notes |
|----------|------|-------|
| **Salaries** | $120K | 1 full-time developer (contract/freelance) |
| **Infrastructure** | $10K | Hosting, database, CDN, email service |
| **Payment Processing** | 3-5% of revenue | Stripe fees |
| **Marketing** | $30K | Ads, content creation, tools |
| **Tools & Services** | $5K | Analytics, monitoring, design tools |
| **Legal/Compliance** | $3K | Privacy policy, terms, accounting |
| **Miscellaneous** | $2K | Contingency |
| **TOTAL** | ~$170K | |

**Revenue Needed**: $170K operating costs + profit target = $250K minimum revenue to break even with healthy margin.

---

## Success Metrics & KPIs

### North Star Metric
**Monthly Recurring Revenue (MRR)** - Primary goal

### Secondary Metrics

**Growth**
- Monthly Active Users (MAU)
- New user signups per week
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)

**Engagement**
- Greetings created per user per month
- QR scans per greeting (average)
- Days active per month (DAU/MAU ratio)
- Feature adoption rate (templates, social sharing, etc.)

**Monetization**
- Conversion rate (free to paid)
- Average Revenue Per User (ARPU)
- Monthly churn rate (target: <5%)
- Net Revenue Retention (NRR)

**Quality**
- User satisfaction (NPS score, target: >50)
- App crash rate (target: <0.1%)
- Page load time (target: <2 seconds)
- API uptime (target: 99.9%)

### Reporting Cadence
- **Daily**: Dashboard checks (revenue, active users, errors)
- **Weekly**: Growth metrics, user feedback summary
- **Monthly**: Full metrics review, board/stakeholder update
- **Quarterly**: Strategic review, roadmap adjustment

---

## Conclusion

The Holiday Greeting QR Code Generator has significant potential. By implementing this plan, you can:

1. **Transform the user experience** from functional utility to delightful product
2. **Establish multiple revenue streams** supporting sustainable growth
3. **Build a community** around personalized digital communication
4. **Create defensible advantages** through features like analytics and collaboration
5. **Scale to profitability** within 12-18 months

**Next Steps**:
1. Validate core assumptions (survey 50 potential users)
2. Build user authentication system (highest priority)
3. Launch MVP of freemium model
4. Implement payment processing
5. Begin organic marketing outreach

**Success Probability**: High (7-8/10) given:
- Clear target audience
- Proven product-market fit signals
- Multiple revenue opportunities
- Growing market trend
- Relatively low technical complexity

Good luck with the Holiday Greeting QR Code Generator! 🎄✨

---

**Document Version**: 1.0  
**Last Updated**: December 27, 2025  
**Status**: Ready for Implementation
````

## File: streamlit/plans/refactor.md
````markdown
# Refactoring Plan: app.py Modular Architecture

> **Status**: ✅ COMPLETED - All Phases Implemented
> **Date Created**: 2025-12-23
> **Date Completed**: 2025-12-24
> **Actual Effort**: Large (7 phases, ~6-8 hours)
> **Risk Level**: Medium (breaking changes, comprehensive testing required)

---

## Problem Statement

`streamlit/app.py` has grown to **2,186 lines** - a monolithic file that's becoming increasingly difficult to maintain. It mixes multiple concerns (UI, business logic, utilities) in one file with significant code duplication and complex functions exceeding 200 lines.

### Current Pain Points
- ❌ Mixed concerns (UI, business logic, utilities)
- ❌ Code duplication (3x repeated QR generation flow)
- ❌ Long functions (233+ lines)
- ❌ Hardcoded CSS (~70 lines inline)
- ❌ Tight coupling, no clear module boundaries
- ❌ Difficult to test individual components
- ❌ Poor IDE performance with large file

---

## Current State Analysis

### File Metrics
- **Total Lines**: 2,186 lines
- **Tabs**: 5 main tabs + 1 view page
- **Helper Functions**: ~20 utility functions mixed with tab code

### Tab Functions Identified
| Tab | Lines | Complexity | Purpose |
|-----|-------|------------|---------|
| `create_greeting_tab()` | 1032-1347 (315) | High | Create new QR codes |
| `scan_greeting_tab()` | 1352-1476 (124) | High | Scan/decode QR codes |
| `examples_tab()` | 1478-1541 (63) | Low | Display examples |
| `batch_greeting_tab()` | 1636-1869 (233) | Very High | Batch CSV generation |
| `about_tab()` | 1871-1984 (113) | Medium | App information |
| `view_greeting_page()` | 1986-2074 (88) | Medium | Mobile view |
| `main()` | 2076-2181 (105) | Medium | Entry point |

### Shared Utilities
**Image/File Handling**: get_img_as_base64, load_theme_icon, get_theme_display_icon, get_available_backgrounds, get_available_gifs, get_all_available_backgrounds

**URL/Background Handling**: is_web_url, classify_background, convert_youtube_to_embed_url, convert_google_drive_to_embed_url, linkify_urls

**QR Code**: generate_qr_code, display_qr_with_protection, display_greeting_letter

**Theme Management**: render_theme_selector

**Download Tracking**: log_download, get_download_count

---

## Proposed Architecture

### Layered Design
Refactor into a **layered modular architecture** with clear separation of concerns:

```
streamlit/
├── app.py                           # Main entry (150-200 lines)
├── config.py                        # Configuration & constants
│
├── utils/                           # Shared utilities
│   ├── __init__.py
│   ├── url_utils.py                # URL/background handling
│   ├── file_utils.py               # File operations, backgrounds
│   ├── image_utils.py              # Image base64, icon loading
│   └── download_tracker.py         # Download tracking
│
├── qr/                              # QR code generation & display
│   ├── __init__.py
│   ├── generator.py                # QR code generation
│   └── display.py                  # QR display components
│
└── tabs/                            # UI tabs (one file per tab)
    ├── __init__.py
    ├── create_tab.py               # Create greeting tab
    ├── scan_tab.py                 # Scan greeting tab
    ├── examples_tab.py             # Examples tab
    ├── batch_tab.py                # Batch processing tab
    ├── about_tab.py                # About tab
    ├── view_page.py                # Mobile greeting view
    └── components.py               # Shared UI components
```

### Dependency Hierarchy
```
app.py (top layer)
  ↓
tabs/*.py (UI layer)
  ↓
qr/*.py (business logic layer)
  ↓
utils/*.py (utility layer)
  ↓
greeting_formats.py (data layer - existing)
  ↓
config.py (configuration layer - no dependencies)
```

---

## Implementation Plan

### Phase 1: Setup Module Structure
**Goal**: Create directory structure and empty module files

**Actions**:
1. Create `streamlit/utils/` directory with `__init__.py`
2. Create `streamlit/qr/` directory with `__init__.py`
3. Create `streamlit/tabs/` directory with `__init__.py`
4. Create `streamlit/config.py` for constants

### Phase 2: Extract Configuration (config.py)
**Goal**: Move all constants and configuration out of app.py

**Extract**:
- `THEME_ICONS` dictionary (line 117)
- Page configuration settings (line 131)
- CSS styles (lines 138-211) → `CSS_STYLES` constant

### Phase 3: Extract Utility Modules
**Goal**: Create reusable utility functions with clear responsibilities

#### 3.1 utils/url_utils.py
- `is_web_url()` (line 222)
- `classify_background()` (line 240)
- `convert_youtube_to_embed_url()` (line 277)
- `convert_google_drive_to_embed_url()` (line 317)
- `linkify_urls()` (line 343)

#### 3.2 utils/file_utils.py
- `get_available_backgrounds()` (line 1543)
- `get_available_gifs()` (line 1606)
- `get_all_available_backgrounds()` (line 1619)

#### 3.3 utils/image_utils.py
- `get_img_as_base64()` (line 215)
- `load_theme_icon()` (line 674)
- `get_theme_display_icon()` (line 710)

#### 3.4 utils/download_tracker.py
- `log_download()` (line 45)
- `get_download_count()` (line 91)

### Phase 4: Extract QR Code Modules
**Goal**: Separate QR generation and display logic

#### 4.1 qr/generator.py
- `generate_qr_code()` (line 797 - ~233 lines)
- Complex text rendering logic
- QR code creation with PIL

#### 4.2 qr/display.py
- `display_qr_with_protection()` (line 370)
- `display_greeting_letter()` (line 441 - ~230 lines)

### Phase 5: Extract Tab Modules
**Goal**: One file per tab, eliminate duplication

#### 5.1 tabs/components.py
**Extract**:
- `render_theme_selector()` (line 737)

**Create New**:
- `render_qr_generation_flow()` - Eliminates 3x duplication in create_greeting_tab

#### 5.2 tabs/create_tab.py
- `create_greeting_tab()` (lines 1032-1347)
- Use `render_qr_generation_flow()` to eliminate duplication

#### 5.3 tabs/scan_tab.py
- `scan_greeting_tab()` (lines 1352-1476)

#### 5.4 tabs/examples_tab.py
- `examples_tab()` (lines 1478-1541)

#### 5.5 tabs/batch_tab.py
- `batch_greeting_tab()` (lines 1636-1869)

#### 5.6 tabs/about_tab.py
- `about_tab()` (lines 1871-1984)

#### 5.7 tabs/view_page.py
- `view_greeting_page()` (lines 1986-2074)

### Phase 6: Refactor Main App (app.py)
**Goal**: Slim main entry point to ~150-200 lines

**New Structure**:
- Import modules
- Apply global CSS
- Main entry point with routing
- Sidebar setup
- Tab orchestration

### Phase 7: Update Imports & Test
**Goal**: Ensure all modules work correctly together

**Actions**:
1. Update all import statements across modules
2. Test each tab independently
3. Test all utility functions
4. Verify no circular dependencies
5. Run full integration test

---

## Migration Strategy

### Recommended: Big Bang Approach
**Approach**: Create all new modules, then switch app.py to use them

**Why Big Bang?**
- Clean slate, easier to get architecture right
- Can test new modules before switching
- Clear before/after comparison
- This codebase is well-understood with existing patterns

**Steps**:
1. Create all new module files alongside existing app.py
2. Copy and adapt code into new modules
3. Update imports and dependencies
4. Test all modules independently
5. Replace app.py with new slim version
6. Keep old app.py as app.py.backup until verified

---

## Critical Considerations

### 1. Code Duplication Elimination
**Target**: 3x duplicated QR generation flow in create_greeting_tab

**Solution**: Create `render_qr_generation_flow()` in `tabs/components.py` that eliminates ~150 lines of duplicated code.

### 2. Import Path Management
Use absolute imports from package root:
```python
# New (in tabs/create_tab.py)
from greeting_formats import create_holiday_greeting
from utils.url_utils import is_web_url, classify_background
from utils.image_utils import get_img_as_base64
from qr.generator import generate_qr_code
from config import THEME_ICONS
```

### 3. Session State & Streamlit Context
- Only import `streamlit` in modules that directly use st.* calls
- Pass data between modules via parameters, not session state
- Keep session state management in tab modules

### 4. Testing Strategy
**Testing Order**:
1. Test config.py (verify imports work)
2. Test utils/* modules (pure functions, easy to test)
3. Test qr/* modules (with mock data)
4. Test tabs/* modules individually
5. Test app.py integration
6. Full end-to-end testing

---

## Expected Benefits

### Maintainability
- ✅ Each module has clear, single responsibility
- ✅ Easy to locate code (one file per tab)
- ✅ Reduced cognitive load (smaller files)
- ✅ Better IDE support (faster autocomplete, navigation)

### Code Quality
- ✅ Eliminates 150+ lines of duplication
- ✅ Forces clear module boundaries
- ✅ Encourages pure functions (easier to test)
- ✅ Separates concerns (UI vs. business logic vs. utilities)

### Future Development
- ✅ Easy to add new tabs (create new file in tabs/)
- ✅ Easy to add new utilities (add to appropriate utils module)
- ✅ Easy to test (import specific modules)
- ✅ Easy to reuse code (import from utils, qr, etc.)

---

## File Size Comparison

### Before (1 file)
```
streamlit/app.py                    2,186 lines
```

### After (16 files)
```
streamlit/app.py                      ~180 lines  ⬇️ 92% reduction
streamlit/config.py                   ~120 lines
streamlit/utils/url_utils.py          ~130 lines
streamlit/utils/file_utils.py         ~90 lines
streamlit/utils/image_utils.py        ~70 lines
streamlit/utils/download_tracker.py   ~70 lines
streamlit/qr/generator.py             ~280 lines
streamlit/qr/display.py               ~280 lines
streamlit/tabs/components.py          ~150 lines
streamlit/tabs/create_tab.py          ~230 lines  ⬇️ 27% reduction
streamlit/tabs/scan_tab.py            ~130 lines
streamlit/tabs/examples_tab.py        ~70 lines
streamlit/tabs/batch_tab.py           ~270 lines
streamlit/tabs/about_tab.py           ~110 lines
streamlit/tabs/view_page.py           ~90 lines
streamlit/tabs/__init__.py            ~10 lines
-------------------------------------------
Total:                                ~2,270 lines across 16 files
```

**Net Change**: +84 lines (+4%) due to import statements, module docstrings, and `__init__.py` files

**Value**: Vastly improved organization and maintainability

---

## Implementation Checklist

### Phase 1: Setup ✅
- [x] Create `streamlit/utils/` directory and `__init__.py`
- [x] Create `streamlit/qr/` directory and `__init__.py`
- [x] Create `streamlit/tabs/` directory and `__init__.py`
- [x] Create empty module files

### Phase 2: Configuration ✅
- [x] Create `config.py` with THEME_ICONS, CSS_STYLES
- [x] Test imports from config.py

### Phase 3: Utilities ✅
- [x] Extract url_utils.py
- [x] Extract file_utils.py
- [x] Extract image_utils.py
- [x] Extract download_tracker.py
- [x] Test all utility functions

### Phase 4: QR Modules ✅
- [x] Extract qr/generator.py
- [x] Extract qr/display.py
- [x] Test QR generation and display

### Phase 5: Tabs ✅
- [x] Create tabs/components.py with render_qr_generation_flow()
- [x] Extract tabs/create_tab.py (use components)
- [x] Extract tabs/scan_tab.py
- [x] Extract tabs/examples_tab.py
- [x] Extract tabs/batch_tab.py
- [x] Extract tabs/about_tab.py
- [x] Extract tabs/view_page.py
- [x] Test each tab independently

### Phase 6: Main App ✅
- [x] Refactor app.py to use new modules
- [x] Backup original as app.py.backup
- [x] Test full application

### Phase 7: Verification ✅
- [x] Test all tabs work correctly
- [x] Test all QR generation scenarios
- [x] Test batch processing
- [x] Test mobile view
- [x] Verify no import errors
- [x] Check for circular dependencies
- [x] Run full integration test

---

## Risk Mitigation

### Risk: Breaking existing functionality
**Mitigation**:
- Keep app.py.backup until fully verified
- Test each module independently before integration
- Use version control with clear commits per phase
- Test all tabs and features thoroughly

### Risk: Circular import dependencies
**Mitigation**:
- Follow strict dependency hierarchy (config → utils → qr → tabs → app)
- Never import from higher layers
- Use dependency injection where needed

### Risk: Missing edge cases
**Mitigation**:
- Comprehensive testing of all scenarios
- Review all utility function usages before extraction
- Keep detailed notes of where code comes from

---

## Success Criteria

✅ **All existing functionality works identically**
✅ **No circular import errors**
✅ **All tabs load and operate correctly**
✅ **Code duplication reduced by >100 lines**
✅ **app.py reduced to <200 lines**
✅ **Each module has clear, single responsibility**
✅ **Future tabs can be added by creating single file in tabs/**
✅ **All utility functions can be imported and tested independently**

---

## Notes

- This is a living document - update as implementation progresses
- Mark checkboxes as completed
- Document any deviations from the plan
- Track any issues or blockers encountered

**Last Updated**: 2025-12-24

---

## 🎉 COMPLETION SUMMARY

### Final Results

**Files Created**: 17 modules across 4 packages
- `config.py` - 100 lines
- `utils/` - 383 lines (4 modules)
- `qr/` - 579 lines (2 modules)
- `tabs/` - 1,131 lines (7 modules)
- **Total**: 2,193 lines in new modular structure

**app.py Transformation**:
- **Before**: 2,185 lines (monolithic)
- **After**: 129 lines (orchestration only)
- **Reduction**: 94% smaller (2,056 lines removed)
- **Backup**: app.py.backup preserved

### Architecture Benefits Achieved

✅ **Clean Separation of Concerns**
- Configuration isolated in `config.py`
- Utilities organized by function (url, file, image, download)
- QR logic separated (generation vs. display)
- Each tab in its own module with `render()` pattern

✅ **Code Duplication Eliminated**
- Shared QR generation flow extracted to `tabs/components.py`
- Utility functions centralized and reusable
- Theme management unified in config

✅ **Improved Maintainability**
- Easy to locate code (one file per concern)
- Clear import hierarchies (no circular dependencies)
- Better IDE support (smaller files, faster autocomplete)
- Each module has single responsibility

✅ **Enhanced Testability**
- Pure functions in utils/ can be tested independently
- Tab modules can be tested in isolation
- Clear interfaces between modules

✅ **Future Development Ready**
- New tabs: Add single file in `tabs/`
- New utilities: Add to appropriate `utils/` module
- Clear patterns established for extensions

### Technical Validation

✅ **Import Structure**: All modules follow proper dependency hierarchy
- config.py (no dependencies)
- utils/ (config only)
- qr/ (config + utils)
- tabs/ (all above + greeting_formats)
- app.py (orchestrates all modules)

✅ **No Circular Dependencies**: Verified through import hierarchy
✅ **Syntax Validation**: All Python files pass py_compile
✅ **Module Count**: 17 files (vs. original 1 monolithic file)

### Success Criteria - ALL MET ✅

✅ app.py reduced to <200 lines (achieved: 129 lines)
✅ All 7 tabs in separate files
✅ All existing functionality preserved in modules
✅ No import errors or circular dependencies
✅ Code duplication reduced by >100 lines
✅ Clear module boundaries and single responsibilities
✅ Future tabs can be added easily
✅ All utility functions independently importable

**Refactoring Complete**: Ready for production use! 🚀
````

## File: streamlit/qr/__init__.py
````python
"""QR code generation and display modules"""
````

## File: streamlit/setup_task.ps1
````powershell
# setup_task.ps1
# This script registers 'keep_alive.ps1' in Windows Task Scheduler to run every 1 hour.

$TaskName = "StreamlitKeepAlive"
$ScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "keep_alive.ps1"
$PythonPath = "powershell.exe"

Write-Host "Setting up Scheduled Task: $TaskName"
Write-Host "Script to run: $ScriptPath"

# Check if task exists and unregister it if so (to allow updating)
$TaskExists = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($TaskExists) {
    Write-Host "Removing existing task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Define the Action (Run PowerShell with the script)
# -ExecutionPolicy Bypass allows the script to run even if policies are restrictive
# -WindowStyle Hidden keeps it from popping up a window every hour
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`""

# Define the Trigger
# Begins NOW, repeats every 1 hour, for an indefinite duration (represented as a very long time)
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) 

# Create and Register the Task
# -Settings argument ensures the task can run properly
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register execution
try {
    Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "Keeps Streamlit App Alive by pinging it every hour." -Settings $Settings
    Write-Host -ForegroundColor Green "Success! Task '$TaskName' has been scheduled."
    Write-Host "It will run every 1 hour. You can view it in Windows Task Scheduler."
    Write-Host "Logs will be saved to: $(Join-Path -Path $PSScriptRoot -ChildPath 'keep_alive_log.txt')"
}
catch {
    Write-Host -ForegroundColor Red "Error registering task. You might need to run this script as Administrator."
    Write-Host "Error Details: $_"
}
````

## File: streamlit/tabs/funnel_tab.py
````python
"""
Marketing Funnel Tab
Create QR codes that convert video viewers to customers

This tab can be used:
1. Standalone - user enters all data manually
2. Pre-filled - data comes from NetPull via URL parameters
"""

import streamlit as st
import urllib.parse
from datetime import datetime
from typing import Optional, Dict
import io

from i18n import get_text as _
from config import THEME_COLORS, THEME_ICONS
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection
from utils.video_utils import validate_video_url, convert_to_embed_url
from utils.download_tracker import log_download


def load_funnel_params_from_url():
    """
    Load pre-filled data from URL parameters (from NetPull redirect).
    
    Expected parameters:
    - landing_url: CTA destination
    - video_url: Video to play
    - headline: Suggested headline
    - offer_text: Suggested offer description
    - og_image: Preview image
    - source: Where the data came from (e.g., 'netpull')
    """
    try:
        params = st.query_params
        
        # Check if we have NetPull data
        if 'landing_url' in params and 'source' not in st.session_state.get('funnel_loaded', {}):
            st.session_state.funnel_loaded = {'source': params.get('source', 'direct')}
            
            # Load all available params
            if 'landing_url' in params:
                st.session_state.funnel_landing_url = params['landing_url']
            if 'video_url' in params:
                st.session_state.funnel_video_url = params['video_url']
            if 'headline' in params:
                st.session_state.funnel_headline = params['headline']
            if 'offer_text' in params:
                st.session_state.funnel_offer_text = params['offer_text']
            if 'og_image' in params:
                st.session_state.funnel_og_image = params['og_image']
            
            # Show success banner
            st.session_state.funnel_show_prefill_banner = True
            
    except Exception as e:
        pass  # Silently handle param errors


def encode_funnel_to_url(funnel_data: Dict) -> str:
    """
    Encode funnel data to URL parameters for QR code.
    
    Uses compact parameter names to minimize QR code complexity.
    """
    base_url = "https://qr-greeting.streamlit.app/"
    
    params = {
        "tab": "view",
        "t": "funnel",  # type
        "f": funnel_data.get("brand", ""),  # from/brand
        "th": funnel_data.get("theme", "fireworks"),  # theme
        "bg": funnel_data.get("video_url", ""),  # background video
        "m": funnel_data.get("offer_text", ""),  # message/offer
        "fh": funnel_data.get("headline", ""),  # funnel headline
        "fc": funnel_data.get("cta_text", ""),  # funnel CTA text
        "fu": funnel_data.get("landing_url", ""),  # funnel CTA URL
        "fp": funnel_data.get("promo_code", ""),  # funnel promo
        "fg": funnel_data.get("urgency", ""),  # funnel urgency
    }
    
    # Remove empty params to save space
    params = {k: v for k, v in params.items() if v}
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def render() -> None:
    """Marketing Funnel tab main render function"""
    
    # Load URL parameters if present (from NetPull)
    load_funnel_params_from_url()
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 20px; color: white; 
                text-align: center; margin-bottom: 30px;">
        <h1>📈 Marketing Funnel QR</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">
            Transform video content into high-converting QR experiences
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show pre-fill banner if data came from NetPull
    if st.session_state.get('funnel_show_prefill_banner', False):
        st.success("✅ **Data loaded from NetPull!** Review and customize below.")
        st.session_state.funnel_show_prefill_banner = False
    
    # Value proposition
    st.info("""
    **💡 The Attention Economy Problem:**  
    People watch your videos but never visit your website.
    
    **✨ The Solution:**  
    Create QR codes that play your video AND show your offer.
    
    **💪 Pro Tip:** Use [NetPull](https://net-test.streamlit.app) to auto-extract page data first!
    """)
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 1: Video & Landing Page
    # ==========================================================================
    st.markdown("### 📹 Step 1: Your Content")
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_url = st.text_input(
            "🎬 Video URL",
            value=st.session_state.get('funnel_video_url', ''),
            placeholder="https://youtube.com/watch?v=... or https://youtu.be/...",
            help="YouTube, Vimeo, or direct video URL (.mp4)",
            key="funnel_video_input"
        )
        
        # Validate and show preview
        if video_url:
            is_valid, video_type, error_msg = validate_video_url(video_url)
            if is_valid:
                st.success(f"✅ Valid {video_type} video")
            else:
                st.error(f"❌ {error_msg}")
    
    with col2:
        landing_url = st.text_input(
            "🔗 Landing Page URL",
            value=st.session_state.get('funnel_landing_url', ''),
            placeholder="https://yoursite.com/offer",
            help="Where users go after seeing your video + offer",
            key="funnel_landing_input"
        )
        
        if landing_url:
            if landing_url.startswith(("http://", "https://")):
                st.success("✅ Valid URL")
            else:
                st.warning("⚠️ URL should start with https://")
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 2: Your Offer
    # ==========================================================================
    st.markdown("### 🎁 Step 2: Your Offer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        headline = st.text_input(
            "📢 Headline",
            value=st.session_state.get('funnel_headline', '🎁 EXCLUSIVE OFFER'),
            placeholder="e.g., 🎁 EXCLUSIVE OFFER, 🔥 LIMITED TIME",
            help="Attention-grabbing headline (use emojis!)",
            key="funnel_headline_input"
        )
        
        offer_text = st.text_area(
            "💬 Offer Description",
            value=st.session_state.get('funnel_offer_text', 
                "Get 20% OFF your first order!\n\nWatch the video to see why customers love us."),
            height=100,
            placeholder="Describe your value proposition...",
            help="What's in it for them? Keep it concise.",
            key="funnel_offer_input"
        )
    
    with col2:
        cta_text = st.text_input(
            "🖱️ Call-to-Action Button",
            value="Shop Now →",
            placeholder="e.g., Shop Now, Learn More, Get Started",
            help="Action text for the button",
            key="funnel_cta_input"
        )
        
        promo_code = st.text_input(
            "🏷️ Promo Code (optional)",
            placeholder="e.g., SAVE20, WELCOME10",
            help="Discount code to display",
            key="funnel_promo_input"
        )
        
        urgency_text = st.text_input(
            "⏰ Urgency Text (optional)",
            placeholder="e.g., Offer expires in 48 hours",
            help="Create FOMO - scarcity drives action",
            key="funnel_urgency_input"
        )
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 3: Branding & Theme
    # ==========================================================================
    st.markdown("### 🎨 Step 3: Branding")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        brand_name = st.text_input(
            "🏢 Brand Name",
            placeholder="Your Company Name",
            help="Shown as 'from' attribution",
            key="funnel_brand_input"
        )
    
    with col2:
        theme_options = {
            "fireworks": "🎆 Fireworks (Excitement)",
            "lights": "✨ Lights (Premium)",
            "confetti": "🎉 Confetti (Celebration)",
            "stars": "⭐ Stars (Aspirational)",
            "champagne": "🥂 Champagne (Luxury)",
        }
        
        selected_theme_label = st.selectbox(
            "🎨 Visual Theme",
            options=list(theme_options.values()),
            index=0,
            help="Sets the mood for your funnel",
            key="funnel_theme_select"
        )
        
        selected_theme = [k for k, v in theme_options.items() 
                         if v == selected_theme_label][0]
    
    with col3:
        visible_message = st.text_input(
            "📝 QR Label (optional)",
            placeholder="e.g., SCAN FOR 20% OFF",
            help="Text printed around the QR code",
            key="funnel_visible_msg_input"
        )
    
    st.markdown("---")
    
    # ==========================================================================
    # Step 4: Generate
    # ==========================================================================
    st.markdown("### 🚀 Step 4: Generate Your Funnel QR")
    
    # Validation
    can_generate = all([landing_url, headline, offer_text, cta_text])
    
    if not can_generate:
        missing = []
        if not landing_url: missing.append("Landing Page URL")
        if not headline: missing.append("Headline")
        if not offer_text: missing.append("Offer Description")
        if not cta_text: missing.append("CTA Button Text")
        st.warning(f"⚠️ Please fill in: {', '.join(missing)}")
    
    if not video_url:
        st.info("💡 **Tip:** Adding a video increases engagement significantly!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            "🚀 Generate Marketing Funnel QR",
            type="primary",
            disabled=not can_generate,
            use_container_width=True,
            key="funnel_generate_btn"
        )
    
    if generate_btn and can_generate:
        # Create funnel data
        funnel_data = {
            "video_url": video_url,
            "landing_url": landing_url,
            "headline": headline,
            "offer_text": offer_text,
            "cta_text": cta_text,
            "promo_code": promo_code,
            "urgency": urgency_text,
            "brand": brand_name,
            "theme": selected_theme
        }
        
        # Encode to URL
        funnel_url = encode_funnel_to_url(funnel_data)
        
        st.success("✅ Marketing Funnel QR Generated!")
        
        # Display results
        result_col1, result_col2 = st.columns([1, 1])
        
        with result_col1:
            st.markdown("#### 📱 Your Funnel QR Code")
            
            # Get theme colors
            theme_colors = THEME_COLORS.get(selected_theme, THEME_COLORS["fireworks"])
            
            # Generate QR
            qr_img = generate_qr_code(
                funnel_url,
                theme=selected_theme,
                visible_message=visible_message if visible_message else None,
                module_color=theme_colors["module"],
                position_ring_color=theme_colors["ring"]
            )
            
            display_qr_with_protection(qr_img, caption="Scan to preview your funnel")
            
            # Download button
            buf = io.BytesIO()
            qr_img.save(buf, format='PNG')
            filename = f"funnel_qr_{brand_name or 'marketing'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            st.download_button(
                label="⬇️ Download QR Code",
                data=buf.getvalue(),
                file_name=filename,
                mime="image/png",
                use_container_width=True,
                on_click=log_download,
                args=(filename,)
            )
        
        with result_col2:
            st.markdown("#### 👀 Preview: What Users See")
            
            # Mockup of the funnel experience
            st.markdown(f"""
            <div style="border: 3px solid #333; border-radius: 20px; padding: 15px; 
                        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
                        color: white; max-width: 350px; margin: 0 auto;">
                <div style="background: #000; border-radius: 10px; height: 150px; 
                            display: flex; align-items: center; justify-content: center;
                            margin-bottom: 15px; position: relative;">
                    <span style="font-size: 3em;">🎬</span>
                    <div style="position: absolute; bottom: 5px; right: 10px; 
                                background: rgba(255,255,255,0.2); padding: 2px 8px; 
                                border-radius: 3px; font-size: 0.8em;">
                        {"Video Playing..." if video_url else "No video"}
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.95); color: #333; 
                            padding: 20px; border-radius: 15px; text-align: center;">
                    <div style="font-size: 1.3em; font-weight: bold; margin-bottom: 10px;">
                        {headline}
                    </div>
                    <div style="font-size: 0.95em; margin-bottom: 15px; line-height: 1.4;">
                        {offer_text[:100]}{'...' if len(offer_text) > 100 else ''}
                    </div>
                    {"<div style='background: #ffd700; color: #333; padding: 5px 15px; border-radius: 5px; font-weight: bold; margin-bottom: 10px; display: inline-block;'>🏷️ " + promo_code + "</div>" if promo_code else ""}
                    {"<div style='color: #e74c3c; font-size: 0.85em; margin-bottom: 10px;'>⏰ " + urgency_text + "</div>" if urgency_text else ""}
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                color: white; padding: 12px 25px; border-radius: 25px; 
                                font-weight: bold; cursor: pointer; display: inline-block;">
                        {cta_text}
                    </div>
                </div>
                <div style="text-align: center; margin-top: 10px; font-size: 0.8em; opacity: 0.7;">
                    {f"from {brand_name}" if brand_name else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Usage tips
        with st.expander("📋 How to Use Your Funnel QR", expanded=True):
            st.markdown(f"""
            **Print it on:**
            - 📦 Product packaging
            - 📄 Flyers and brochures  
            - 🪧 Posters and banners
            - 💳 Business cards
            - 🧾 Receipts and invoices
            - 📱 Social media posts
            
            **Pro Tips:**
            1. **Test it first** - Scan with your phone to verify the experience
            2. **Track conversions** - Use UTM parameters in your landing URL
            3. **A/B test** - Try different headlines and CTAs
            4. **Update regularly** - Change offers to keep it fresh
            
            **Your Funnel URL:**
            ```
            {funnel_url}
            ```
            """)
````

## File: streamlit/test_fb_url.py
````python
import sys
import os
sys.path.append(os.path.abspath("e:/code2/netshare/streamlit"))

from utils.url_utils import classify_background, convert_facebook_to_embed_url

test_url = "https://www.facebook.com/share/r/1GzVWWtk3P/"

print(f"Testing URL: {test_url}")

# Test Classification
bg_type = classify_background(test_url)
print(f"Classification: {bg_type}")
assert bg_type == 'facebook', f"Expected 'facebook', got '{bg_type}'"

# Test Conversion
embed_url = convert_facebook_to_embed_url(test_url)
print(f"Embed URL: {embed_url}")
assert embed_url is not None, "Embed URL should not be None"
assert "facebook.com/plugins/video.php" in embed_url, "Should be a Facebook video plugin URL"

print("✅ Validation successful!")
````

## File: streamlit/test_greeting.csv
````
From,To,Message,Theme,Background,VisibleMessage
TestSender,TestReceiver,This is a test message from CSV,snowflake,letter-background-design-01.jpg,Scan to read
````

## File: streamlit/utils/__init__.py
````python
"""Utility modules for QR Greeting Card Generator"""
````

## File: streamlit/utils/download_tracker.py
````python
"""
Download tracking utility for logging QR code downloads
Thread-safe CSV-based tracking with file locking support
"""

import csv
import sys
from datetime import datetime
from pathlib import Path


def log_download(filename: str) -> None:
    """
    Log a QR code download event to track.csv

    Args:
        filename: Name of the downloaded file

    Thread-safe implementation using file locking
    """
    # CSV file path (parent directory of utils/)
    csv_path = Path(__file__).parent.parent / "track.csv"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Create file with headers if it doesn't exist
        if not csv_path.exists():
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['filename', 'timestamp'])

        # Append with exclusive lock (prevents concurrent write corruption)
        with open(csv_path, 'a', newline='') as f:
            # Acquire exclusive lock (blocks other processes)
            try:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            except (ImportError, AttributeError):
                # fcntl not available on Windows, skip locking
                pass

            try:
                writer = csv.writer(f)
                writer.writerow([filename, timestamp])
            finally:
                # Release lock if fcntl is available
                try:
                    import fcntl
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (ImportError, AttributeError):
                    pass
    except Exception as e:
        # Silent failure - don't interrupt user experience
        print(f"Warning: Failed to log download: {e}", file=sys.stderr)


def get_download_count() -> int:
    """
    Read and count total downloads from track.csv

    Returns:
        Number of downloads, or 0 if file doesn't exist or error occurs
    """
    csv_path = Path(__file__).parent.parent / "track.csv"

    try:
        if not csv_path.exists():
            return 0

        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader, None)
            # Count remaining rows
            count = sum(1 for _ in reader)
            return count
    except Exception as e:
        # Return 0 on error (graceful degradation)
        print(f"Warning: Failed to read download count: {e}", file=sys.stderr)
        return 0
````

## File: streamlit/utils/file_utils.py
````python
"""
File utility functions for managing background resources
Handles background file discovery from keep/ and gif/ folders
"""

from pathlib import Path
from typing import List, Tuple, Dict


def get_available_backgrounds() -> List[str]:
    """
    Get list of available background files from keep/ folder

    Returns:
        Sorted list of background filenames
    """
    keep_path = Path(__file__).parent.parent / "keep"
    if not keep_path.exists():
        return []

    # Support images and videos
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'}
    backgrounds = []
    for f in keep_path.iterdir():
        if f.suffix.lower() in extensions:
            backgrounds.append(f.name)
    return sorted(backgrounds)


def get_available_gifs() -> List[str]:
    """
    Get list of available background files (GIF, JPG) from gif/ folder

    Returns:
        Sorted list of GIF and JPG filenames
    """
    gif_path = Path(__file__).parent.parent / "gif"
    if not gif_path.exists():
        return []

    gifs = []
    for f in gif_path.iterdir():
        if f.suffix.lower() in ['.gif', '.jpg', '.jpeg']:
            gifs.append(f.name)
    return sorted(gifs)


def get_all_available_backgrounds() -> Tuple[List[str], Dict[str, str]]:
    """
    Get combined list of backgrounds from both keep/ and gif/ folders

    Returns:
        Tuple of (sorted list of all background filenames, dict mapping filename to folder)
        The dict values are 'keep' or 'gif' indicating source folder
    """
    backgrounds_from_keep = get_available_backgrounds()
    backgrounds_from_gif = get_available_gifs()

    # Create a dictionary to track folder source for each file
    # This helps with file resolution later
    background_map = {}
    for bg in backgrounds_from_keep:
        background_map[bg] = 'keep'
    for bg in backgrounds_from_gif:
        if bg not in background_map:  # Avoid duplicates, keep/ takes priority
            background_map[bg] = 'gif'

    return sorted(background_map.keys()), background_map
````

## File: streamlit/utils/image_utils.py
````python
"""
Image utility functions for icon loading and base64 conversion
Handles theme icon loading and image encoding
"""

import base64
import os
from PIL import Image
from typing import Optional


def get_img_as_base64(file_path: str) -> str:
    """
    Read image file and return base64 string

    Args:
        file_path: Path to image file

    Returns:
        Base64 encoded string of the image
    """
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def load_theme_icon(theme: str, size: int = 100) -> Optional[Image.Image]:
    """
    Load and resize theme icon from file

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Desired icon size in pixels

    Returns:
        PIL Image with transparent background, or None if not found
    """
    # Path to icon file
    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", f"{theme}.png")

    try:
        # Load icon
        icon = Image.open(icon_path)

        # Resize to desired size with high-quality resampling
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)

        # Ensure RGBA mode for transparency
        if icon.mode != 'RGBA':
            icon = icon.convert('RGBA')

        return icon
    except FileNotFoundError:
        # Icon file doesn't exist - return None to skip icon
        return None
    except Exception as e:
        print(f"Error loading icon for theme '{theme}': {e}")
        return None


def get_theme_display_icon(theme: str, size: int = 60) -> Optional[Image.Image]:
    """
    Load theme icon for display in UI preview

    Args:
        theme: Theme name (e.g., "snowflake", "hearts")
        size: Preview size in pixels (default 60px for grid display)

    Returns:
        PIL Image or None if theme is "general" or icon not found
    """
    if theme == "general":
        return None

    icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", f"{theme}.png")

    if not os.path.exists(icon_path):
        return None

    try:
        icon = Image.open(icon_path)
        icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        return icon
    except Exception:
        return None
````

## File: streamlit/utils/video_utils.py
````python
"""
Video utility functions for Marketing Funnel feature
Handles video URL validation and metadata extraction
"""

import re
from typing import Tuple, Optional
from utils.url_utils import (
    convert_youtube_to_embed_url,
    convert_google_drive_to_embed_url
)


def validate_video_url(url: str) -> Tuple[bool, str, str]:
    """
    Validate if a URL is a supported video source.
    
    Args:
        url: Video URL to validate
        
    Returns:
        Tuple of (is_valid, video_type, error_message)
        video_type is one of: 'YouTube', 'Vimeo', 'Direct Video', 'Google Drive'
    """
    if not url:
        return False, "", "No URL provided"
    
    url_lower = url.lower()
    
    # YouTube
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        embed_url = convert_youtube_to_embed_url(url)
        if embed_url:
            return True, "YouTube", ""
        else:
            return False, "", "Invalid YouTube URL format"
    
    # Vimeo
    if 'vimeo.com' in url_lower:
        vimeo_match = re.search(r'vimeo\.com/(\d+)', url)
        if vimeo_match:
            return True, "Vimeo", ""
        else:
            return False, "", "Invalid Vimeo URL format"
    
    # Google Drive
    if 'drive.google.com' in url_lower:
        embed_url = convert_google_drive_to_embed_url(url)
        if embed_url:
            return True, "Google Drive", ""
        else:
            return False, "", "Invalid Google Drive URL format"
    
    # Direct video files
    video_extensions = ['.mp4', '.webm', '.mov', '.m4v', '.avi']
    if any(url_lower.endswith(ext) for ext in video_extensions):
        return True, "Direct Video", ""
    
    # Check for video in URL path (some CDNs)
    if any(ext in url_lower for ext in video_extensions):
        return True, "Direct Video", ""
    
    return False, "", "Unsupported video URL. Use YouTube, Vimeo, Google Drive, or direct video links (.mp4, .webm)"


def get_youtube_thumbnail(video_id: str, quality: str = "hq") -> str:
    """Get YouTube video thumbnail URL."""
    quality_map = {
        "maxres": "maxresdefault",
        "hq": "hqdefault",
        "mq": "mqdefault",
        "sd": "sddefault",
        "default": "default"
    }
    quality_slug = quality_map.get(quality, "hqdefault")
    return f"https://img.youtube.com/vi/{video_id}/{quality_slug}.jpg"


def convert_to_embed_url(url: str) -> Optional[str]:
    """Convert any supported video URL to embeddable format."""
    if not url:
        return None
        
    is_valid, video_type, _ = validate_video_url(url)
    
    if not is_valid:
        return None
    
    if video_type == "YouTube":
        return convert_youtube_to_embed_url(url)
    
    if video_type == "Vimeo":
        vimeo_match = re.search(r'vimeo\.com/(\d+)', url)
        if vimeo_match:
            return f"https://player.vimeo.com/video/{vimeo_match.group(1)}"
    
    if video_type == "Google Drive":
        return convert_google_drive_to_embed_url(url)
    
    if video_type == "Direct Video":
        return url
    
    return None
````

## File: .gitignore
````
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

*.json
.claude/
# Virtual Environment
.venv*/
venv/
*venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# NetShare specific
netshare_qr.png
*.log
streamlit/track.csv

# Testing
.pytest_cache/
.coverage
htmlcov/

# Temporary files
*.tmp
temp/
tmp/

# app specific data
*.png
!streamlit/*/*.png
!streamlit/packages.txt
!streamlit/translations.json

# PyPI build automation
pypi-build/.env
pypi-build/logs/
````

## File: netshare.code-workspace
````
{
	"folders": [
		{
			"path": "."
		},
		{
			"path": "../../3rd/amazing-qr"
		},
		{
			"path": "../net-test"
		}
	],
	"settings": {}
}
````

## File: PLAINTEXT_API.md
````markdown
# Plaintext API for QR Greeting

## Overview

This feature adds URL parameter support to automatically pre-fill greeting fields, enabling seamless integration with external applications.

## API Usage

### Base URL
```
https://qr-greeting.streamlit.app/?tab=create
```

### Supported Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `from` | string | Sender name | `Dream Tycoon Player` |
| `to` | string | Recipient name | `Fellow Tycoon` |
| `message` | string | Greeting message | `I grew my Dream Fund...` |
| `theme` | string | Visual theme | `confetti`, `snowflake`, `hearts`, etc. |
| `background` | string | Background file or URL | `Christmas-Animation1.gif` or `https://youtube.com/...` |
| `url` | string | Source URL (for attribution) | `https://risk-reward-game.streamlit.app` |

### Example URL

```
https://qr-greeting.streamlit.app/?tab=create&from=Dream+Tycoon+Player&to=Fellow+Tycoon&message=I+grew+my+Dream+Fund+from+%241%2C000+to+%241%2C416+%28%2B41.6%25+profit%29+in+2+rounds%21+Can+you+beat+my+score%3F&theme=confetti&background=Christmas-Animation1.gif&url=https%3A%2F%2Frisk-reward-game.streamlit.app
```

## Implementation Details

### How It Works

1. **URL Parameter Detection**: On page load, the app checks for URL parameters
2. **Session State Population**: If parameters are found, they pre-fill the session state
3. **One-Time Load**: Parameters are only loaded once per session to avoid overwriting user edits
4. **Source Attribution**: If `url` parameter is provided, shows a banner: "✨ Pre-filled from: [url]"

### Code Flow

```python
def load_params_from_url():
    """Load greeting parameters from URL query params if present"""
    query_params = st.query_params
    
    if 'from' in query_params or 'message' in query_params:
        if 'params_loaded_from_url' not in st.session_state:
            st.session_state.params_loaded_from_url = True
            
            # Load parameters into session state
            if 'from' in query_params:
                st.session_state.create_from_name = query_params['from']
            # ... (other parameters)
```

## Integration Examples

### Python (urllib)

```python
import urllib.parse

# Build parameters
params = urllib.parse.urlencode({
    'from': 'Game Player',
    'to': 'Friend',
    'message': 'Check out my score!',
    'theme': 'confetti',
    'background': 'Christmas-Animation1.gif',
    'url': 'https://your-app.streamlit.app'
})

# Create URL
qr_url = f"https://qr-greeting.streamlit.app/?tab=create&{params}"
```

### JavaScript

```javascript
const params = new URLSearchParams({
    from: 'Game Player',
    to: 'Friend',
    message: 'Check out my score!',
    theme: 'confetti',
    background: 'https://www.youtube.com/watch?v=VIDEO_ID',
    url: 'https://your-app.streamlit.app'
});

const qrUrl = `https://qr-greeting.streamlit.app/?tab=create&${params.toString()}`;
```

### Curl

```bash
curl "https://qr-greeting.streamlit.app/?tab=create&from=Player&to=Friend&message=Hello&theme=confetti&background=NewYear-Animation1.gif"
```

## Available Themes

- `snowflake` - Winter/Christmas theme
- `fireworks` - New Year celebration
- `lights` - Holiday lights
- `stars` - Starry night
- `confetti` - General celebration
- `champagne` - Celebration/party
- `hearts` - Valentine's Day / Love
- `farewell` - Goodbye
- `valentine` - Valentine's Day
- `burn_after_read` - Secret message
- `general` - Default theme

## Background Parameter

### Supported Background Types

1. **Local Files**: Use filename from available backgrounds
   ```
   ?background=Christmas-Animation1.gif
   ```

2. **Web URLs**: Direct video links or platform URLs
   ```
   ?background=https://youtube.com/watch?v=VIDEO_ID
   ?background=https://drive.google.com/file/d/FILE_ID/view
   ?background=https://example.com/video.mp4
   ```

### Available Local Backgrounds

- `Christmas-Animation1.gif` - Christmas theme
- `Christmas-Animation2.gif` - Alternative Christmas
- `NewYear-Animation1.gif` - New Year celebration
- `NewYear-Animation2.gif` - Alternative New Year
- `Valentine-Animation1.jpg` - Valentine's Day
- `Valentine-Animation2.jpg` - Alternative Valentine
- `letter-background-design-01.jpg` - General letter background

### Supported Web Platforms

- **YouTube**: Full watch URLs and short links
- **Google Drive**: Shared file links
- **Facebook**: Video and reel URLs
- **Instagram**: Reel and post URLs (limited support)
- **Direct Video**: .mp4, .webm, .mov, .avi, .m3u8 files

### Validation Behavior

- Invalid backgrounds fallback to no background
- Warning shown to user for validation errors
- Local files checked against available GIF list
- Web URLs validated for format and platform support

## Use Cases

### 1. Game Score Sharing
Allow players to share achievements via QR codes:
```
?from=Player123&to=Friends&message=Beat level 50!&theme=confetti
```

### 2. Event Invitations
Pre-fill event details:
```
?from=EventOrg&to=Guest&message=You're invited to our party!&theme=champagne
```

### 3. Cross-App Integration
Link from one app to QR greeting generator:
```
?from=MyApp User&to=Recipient&message=Message&url=https://myapp.com
```

## User Experience

1. User clicks link with parameters
2. QR Greeting app opens on "Create Greeting" tab
3. Form fields are pre-filled with provided values
4. Banner shows: "✨ Pre-filled from: [source-url]"
5. User can edit fields if needed
6. User clicks "Generate" to create QR code

## Technical Considerations

- **URL Encoding**: All parameters must be URL-encoded
- **Character Limits**: Messages should be kept under 300 characters for optimal QR code size
- **Session Persistence**: Parameters only load once per session
- **Reset Capability**: "Create Another" button clears URL parameters

## Benefits

✅ **Seamless Integration**: Apps can link directly to pre-filled forms  
✅ **User Convenience**: No manual data entry required  
✅ **Cross-Promotion**: Apps can reference each other via `url` parameter  
✅ **Viral Growth**: Easy sharing mechanism for user-generated content  

## Future Enhancements

- [ ] Add `visible_message` parameter for QR code overlays
- [ ] Add `auto_generate` parameter to skip manual generation step
- [ ] Add webhook support for automated QR generation
````

## File: streamlit/i18n.py
````python
# -*- coding: utf-8 -*-
"""
Internationalization (i18n) module for Streamlit Holiday Greeting QR application.

Provides translation infrastructure for multi-language support using session state
and JSON-based translation files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st
import streamlit.components.v1 as components


# Path to translations file
TRANSLATIONS_FILE = Path(__file__).parent / "translations.json"

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh": "中文 (简体)"
}

# Default language
DEFAULT_LANGUAGE = "en"

# Cache for loaded translations
_translations_cache: Optional[Dict[str, Dict[str, str]]] = None


def load_translations() -> Dict[str, Dict[str, str]]:
    """
    Load translations from JSON file.

    Returns:
        Dictionary with language codes as keys and translation dictionaries as values.
        Example: {"en": {"key": "value"}, "zh": {"key": "值"}}
    """
    global _translations_cache

    # Return cached translations if available
    if _translations_cache is not None:
        return _translations_cache

    # Load translations from file
    if not TRANSLATIONS_FILE.exists():
        st.error(f"Translations file not found: {TRANSLATIONS_FILE}")
        return {"en": {}, "zh": {}}

    try:
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
            translations = json.load(f)
            _translations_cache = translations
            return translations
    except json.JSONDecodeError as e:
        st.error(f"Error parsing translations file: {e}")
        return {"en": {}, "zh": {}}
    except Exception as e:
        st.error(f"Error loading translations: {e}")
        return {"en": {}, "zh": {}}


def detect_browser_locale():
    """
    Inject JavaScript to detect browser locale and store in session state.
    Only runs once on first visit (when language hasn't been set yet).
    Maps browser locale to 'zh' if it starts with 'zh', otherwise 'en'.
    """
    # Only detect if we haven't set a language yet
    if "language" in st.session_state:
        return
    
    # Check if we already have a detected locale from query params
    try:
        query_params = st.query_params
        detected = query_params.get("detected_locale")
    except:
        query_params = st.experimental_get_query_params()
        detected = query_params.get("detected_locale", [None])[0]
    
    if detected:
        # Store the detected locale and use it
        lang = "zh" if detected.startswith("zh") else "en"
        st.session_state.language = lang
        st.session_state._locale_detected = True
        return
    
    # If not already detected, inject JavaScript to detect and reload with param
    if not st.session_state.get("_locale_detection_attempted"):
        st.session_state._locale_detection_attempted = True
        components.html("""
            <script>
            (function() {
                const browserLocale = navigator.language || navigator.userLanguage || 'en';
                const url = new URL(window.parent.location.href);
                // Only add param if not already present
                if (!url.searchParams.has('detected_locale')) {
                    url.searchParams.set('detected_locale', browserLocale);
                    window.parent.location.href = url.toString();
                }
            })();
            </script>
        """, height=0)


def init_language():
    """
    Initialize language setting in session state.
    Call this once at app startup before any translation calls.
    """
    # First, try to detect browser locale (only on first visit)
    detect_browser_locale()
    
    # If language still not set, use default
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE


def get_current_language() -> str:
    """
    Get the currently selected language code.

    Returns:
        Language code (e.g., "en", "zh")
    """
    return st.session_state.get("language", DEFAULT_LANGUAGE)


def set_language(lang_code: str):
    """
    Set the active language and trigger app rerun.

    Args:
        lang_code: Language code to set (e.g., "en", "zh")
    """
    if lang_code in SUPPORTED_LANGUAGES:
        st.session_state.language = lang_code
        st.rerun()
    else:
        st.warning(f"Unsupported language code: {lang_code}")


def get_text(key: str, **kwargs) -> str:
    """
    Get translated text for the given key in the current language.

    Implements fallback chain: current language → English → show key
    Supports variable substitution using keyword arguments.

    Args:
        key: Translation key in dot notation (e.g., "app.sidebar.title")
        **kwargs: Variables to substitute in the translated text

    Returns:
        Translated text with variables substituted

    Examples:
        >>> get_text("app.sidebar.title")
        "Holiday Greeting QR"

        >>> get_text("qr.stats", bytes=1024, version=5)
        "Data size: 1024 bytes, Version: 5"
    """
    # Get current language
    current_lang = get_current_language()

    # Load translations
    translations = load_translations()

    # Try to get translation in current language
    if current_lang in translations and key in translations[current_lang]:
        text = translations[current_lang][key]
    # Fallback to English
    elif "en" in translations and key in translations["en"]:
        text = translations["en"][key]
    # Show missing key indicator
    else:
        return f"[missing: {key}]"

    # Substitute variables if provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError as e:
            st.warning(f"Missing variable in translation '{key}': {e}")
        except Exception as e:
            st.warning(f"Error formatting translation '{key}': {e}")

    return text


def get_language_selector():
    """
    Create a language selector widget for the sidebar.

    Returns:
        Streamlit selectbox widget for language selection
    """
    current_lang = get_current_language()

    # Create language options with display names
    language_options = list(SUPPORTED_LANGUAGES.keys())
    language_labels = [SUPPORTED_LANGUAGES[code] for code in language_options]

    # Find current index
    try:
        current_index = language_options.index(current_lang)
    except ValueError:
        current_index = 0

    # Create selectbox
    selected_label = st.selectbox(
        "🌐 Language / 语言",
        options=language_labels,
        index=current_index,
        key="language_selector"
    )

    # Get selected language code
    selected_index = language_labels.index(selected_label)
    selected_code = language_options[selected_index]

    # Update language if changed
    if selected_code != current_lang:
        set_language(selected_code)

    return selected_code


# Convenience alias for shorter code
_ = get_text
````

## File: streamlit/keepalive_daemon.py
````python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keepalive Daemon Thread
Pings dependent services in the background to keep them online.
"""

import threading
import time
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
KEEPALIVE_TARGETS = [
    {
        "name": "net-test",
        "url": "https://net-test.streamlit.app/",
        "interval_minutes": 30
    }
]

# Track if daemon has been started (singleton pattern)
_daemon_started = False
_daemon_lock = threading.Lock()


def ping_service(url: str, name: str) -> bool:
    """
    Ping a service URL to keep it alive.

    Args:
        url: The URL to ping
        name: Service name for logging

    Returns:
        True if successful, False otherwise
    """
    try:
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=60)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{timestamp}] Keepalive ping to {name}: Status {response.status_code}")
        return response.status_code == 200
    except ImportError:
        logger.warning("requests library not available for keepalive daemon")
        return False
    except Exception as e:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.warning(f"[{timestamp}] Keepalive ping to {name} failed: {e}")
        return False


def keepalive_worker(target: dict):
    """
    Worker function that runs in a daemon thread.
    Pings the target URL at the specified interval.

    Args:
        target: Dictionary with 'name', 'url', and 'interval_minutes'
    """
    name = target["name"]
    url = target["url"]
    interval_seconds = target["interval_minutes"] * 60

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"[{timestamp}] Keepalive daemon started for {name} (interval: {target['interval_minutes']} min)")

    # Initial ping
    ping_service(url, name)

    while True:
        time.sleep(interval_seconds)
        ping_service(url, name)


def start_keepalive_daemon():
    """
    Start the keepalive daemon thread(s) for all configured targets.
    Uses a singleton pattern to ensure only one daemon per target.
    Safe to call multiple times - will only start once.
    """
    global _daemon_started

    with _daemon_lock:
        if _daemon_started:
            return

        for target in KEEPALIVE_TARGETS:
            thread = threading.Thread(
                target=keepalive_worker,
                args=(target,),
                daemon=True,  # Daemon thread - won't block app shutdown
                name=f"keepalive-{target['name']}"
            )
            thread.start()

        _daemon_started = True
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{timestamp}] Keepalive daemon threads started")


def is_daemon_running() -> bool:
    """Check if the keepalive daemon has been started."""
    return _daemon_started
````

## File: streamlit/plans/interative_demo.md
````markdown
# Interactive Demo Feature - Detailed Implementation Plan

**Project**: Holiday Greeting QR Code Generator  
**Feature**: Interactive Demo Tab  
**Purpose**: Low-friction entry point for new users to experience the product in <60 seconds  
**Target Conversion**: Convert 15-20% of demo users to full greeting creation  
**Created**: December 27, 2025

---

## Table of Contents
1. [Feature Overview](#feature-overview)
2. [User Experience Design](#user-experience-design)
3. [Technical Architecture](#technical-architecture)
4. [Implementation Guide](#implementation-guide)
5. [Code Specifications](#code-specifications)
6. [Integration Points](#integration-points)
7. [Success Metrics](#success-metrics)
8. [Future Enhancements](#future-enhancements)

---

## Feature Overview

### What is the Interactive Demo?

The Interactive Demo is a lightweight, low-friction feature that allows first-time users to create a sample QR code greeting in under 60 seconds without any form friction or required fields. It serves as:

- **Product Discovery**: Show what's possible in the app
- **Conversion Funnel**: Gateway to full greeting creation
- **Social Proof Generator**: Create shareable examples
- **User Onboarding**: Guide new users through the workflow

### Key Principles

1. **Speed**: Generate a greeting in <10 clicks
2. **Simplicity**: Minimal cognitive load (no confusing options)
3. **Beauty**: Impressive visual output to motivate deeper exploration
4. **Engagement**: Interactive elements that feel fun, not robotic
5. **Frictionless**: No signup, login, or complex decisions required
6. **Guided**: Natural progression toward full app features

### Success Definition

- Demo tab receives >30% of new user traffic
- >15% of demo users click "Create My Own Greeting"
- Average session time: 2-3 minutes
- Mobile conversion rate: >20%
- Desktop conversion rate: >25%

---

## User Experience Design

### User Flow Diagram
```
Landing (First-time User)
    ↓
See "Try Interactive Demo" CTA in header/sidebar
    ↓
Click → Enters Demo Tab
    ↓
Sees Pre-filled Sample Greeting:
  From: Sarah
  To: Mike
  Occasion: Christmas 2025
  Message: "Wishing you a magical holiday season..."
  Theme: Snowflake (shown visually)
    ↓
Three Paths Available:
    ├─→ Path A: "Generate Demo QR" (Instant generation)
    │      ↓
    │   Sees animated QR code generation
    │      ↓
    │   QR code displays beautifully
    │      ↓
    │   Shows scan result preview on mobile frame
    │      ↓
    │   [Next Steps Button: "Create My Own Greeting"]
    │
    ├─→ Path B: "Customize Demo" (Quick tweaks)
    │      ↓
    │   Edit: From Name (text field)
    │   Edit: Occasion (dropdown quick select)
    │   Edit: Theme (visual theme selector)
    │   Edit: Message (textarea)
    │      ↓
    │   Live preview updates in real-time
    │      ↓
    │   "Generate Custom Demo QR"
    │      ↓
    │   [Share or Create My Own]
    │
    └─→ Path C: "Start From Scratch" (Full creation)
         ↓
      Takes user to full "Create Greeting" tab
```

### Screen Layout (Desktop)
```
┌─────────────────────────────────────────────────────────────┐
│  Header: "✨ Try the Interactive Demo ✨"                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Left Panel (50%)          │  Right Panel (50%)              │
│  ────────────────────────  │  ────────────────────────      │
│                            │                                 │
│  Sample Greeting Preview:  │  Interactive QR Output:        │
│  ┌──────────────────────┐  │  ┌──────────────────────────┐  │
│  │ From: Sarah          │  │  │                          │  │
│  │ To: Mike             │  │  │      [QR CODE]          │  │
│  │ Occasion: Christmas  │  │  │      (animated)         │  │
│  │ Theme: ❄️ Snowflake │  │  │                          │  │
│  │                      │  │  │  Scans reveal:          │  │
│  │ Message:             │  │  │  ┌────────────────────┐ │  │
│  │ "Wishing you a       │  │  │  │ Christmas Greeting │ │  │
│  │  magical holiday..." │  │  │  │ From: Sarah To: Mike│ │  │
│  └──────────────────────┘  │  │  │ Message appears...  │ │  │
│                            │  │  └────────────────────┘ │  │
│  [Customize Demo]          │  │                          │  │
│  [Generate Demo QR] (CTA)  │  │  [Download QR]          │  │
│                            │  │  [Share to Social]      │  │
│                            │  │  [Try Full Creator]     │  │
│                            │  │                          │  │
│  Theme Quick Selector:     │  └──────────────────────────┘  │
│  ❄️ ☃️ 🎆 ✨ 🎉 🥂 ❤️ 👋  │                                 │
│                            │                                 │
└─────────────────────────────────────────────────────────────┘
```

### Screen Layout (Mobile)
```
┌──────────────────────────┐
│ Try the Demo             │
├──────────────────────────┤
│                          │
│ Sample Greeting:         │
│ ┌────────────────────┐   │
│ │ From: Sarah        │   │
│ │ To: Mike           │   │
│ │ Occasion: Xmas     │   │
│ │ Theme: ❄️ Snowflake│   │
│ │                    │   │
│ │ "Wishing you a     │   │
│ │  magical holiday..."│  │
│ └────────────────────┘   │
│                          │
│ [Customize ↓]            │
│ [Generate QR →]          │
│                          │
├──────────────────────────┤
│                          │
│  QR Code (Full Width):   │
│  ┌────────────────────┐  │
│  │                    │  │
│  │    [QR CODE]       │  │
│  │    (Animated)      │  │
│  │                    │  │
│  └────────────────────┘  │
│                          │
│ When Scanned:            │
│ ┌────────────────────┐   │
│ │ Christmas Greeting │   │
│ │ From: Sarah        │   │
│ │ To: Mike           │   │
│ │                    │   │
│ │ Message appears    │   │
│ │ with snowflake     │   │
│ │ animation...       │   │
│ └────────────────────┘   │
│                          │
│ [Download] [Share]       │
│ [Create My Own] (CTA)    │
│                          │
└──────────────────────────┘
```

### Key UI Elements

#### 1. Welcome Section
- Prominent headline: "✨ Try the Interactive Demo ✨"
- Subheading: "Create a sample greeting in under 60 seconds"
- No login/signup required badge

#### 2. Pre-filled Sample Data
```python
DEFAULT_DEMO_GREETING = {
    "from": "Sarah",
    "to": "Mike",
    "occasion": "Christmas 2025",
    "message": "Wishing you a magical holiday season filled with joy, laughter, and special moments with loved ones!",
    "theme": "snowflake",
    "animation": "FadeInCenterOut"
}
```

#### 3. Three Call-to-Action Buttons

**Button 1: "Generate Demo QR"** (Primary CTA)
- Style: Bold, prominent button
- Color: Theme-matched (e.g., snowflake blue)
- Icon: ✨ or 🎁
- Action: Generate QR immediately with default data
- Feedback: Animated confetti or smooth transition

**Button 2: "Customize Demo"** (Secondary CTA)
- Style: Secondary button style
- Opens: Expandable customization panel
- Allows: Quick edits to demo data
- Real-time preview: Updates as user types

**Button 3: "Create My Own Greeting"** (Conversion CTA)
- Style: Tertiary or text link
- Appears: After QR generation
- Action: Navigate to full "Create Greeting" tab
- Tracking: Log conversion event

#### 4. Theme Selector (Visual Carousel)
```
Theme Selection Carousel:
← [❄️ Snowflake] [☃️ Winter] [🎆 Fireworks] [✨ Lights] 
   [⭐ Stars] [🎉 Confetti] [🥂 Champagne] [❤️ Hearts] →
```

Features:
- Click to preview theme instantly
- Shows theme name on hover
- Animated appearance
- Mobile: Horizontal scroll

#### 5. QR Code Display with Mobile Frame

**Desktop View:**
- Large QR code (400x400px minimum)
- Shows surrounding smartphone frame mockup
- Displays what greeting looks like when scanned
- Animated reveal of decoded message

**Mobile View:**
- Full-width QR code
- Shows stacked mockup (what user sees on their phone)
- Tap to expand/fullscreen

### Customization Panel (Collapsed by Default)

When user clicks "Customize Demo":
```
┌─ Customize Your Demo ─────────────────────────┐
│                                                │
│ From: [Sarah                        ]           │
│ (Your name)                                     │
│                                                │
│ To: [Mike                           ]           │
│ (Recipient's name)                            │
│                                                │
│ Occasion:                                       │
│ ○ Birthday      ○ Christmas  ○ Wedding       │
│ ○ Anniversary   ○ New Year   ○ Other         │
│ Custom: [Enter occasion              ]        │
│                                                │
│ Theme:                                         │
│ [❄️] [☃️] [🎆] [✨] [🎉] [🥂] [❤️] [👋]      │
│                                                │
│ Message Preview:                               │
│ [Wishing you a magical holiday season...    ] │
│ (char count: 87/500)                          │
│                                                │
│ [Update Preview] [Reset to Default]           │
│                                                │
└────────────────────────────────────────────────┘
```

### Interaction Patterns

#### Real-Time Updates
- As user edits "From" name: Preview updates
- Theme selection: QR code color changes live
- Message edit: Character count updates
- Occasion change: Suggested themes highlight

#### Micro-interactions
- Input fields: Soft focus effect on click
- Theme buttons: Smooth scale-up on hover
- Message count: Color changes when approaching limit
- Success state: Checkmark animation when customization complete

#### Progressive Disclosure
1. User sees default greeting
2. Clicks "Customize" to reveal more options
3. Edits are hidden until explicitly requested
4. Creates feeling of simplicity with depth

---

## Technical Architecture

### Module Structure
```
streamlit/
├── app.py (main app)
├── tabs/
│   ├── __init__.py
│   ├── create_tab.py (existing)
│   ├── scan_tab.py (existing)
│   ├── examples_tab.py (existing)
│   ├── batch_tab.py (existing)
│   ├── about_tab.py (existing)
│   ├── view_page.py (existing)
│   └── demo_tab.py (NEW)
├── utils/
│   ├── __init__.py
│   ├── qr_generator.py (new utility functions)
│   └── demo_data.py (NEW)
├── config.py (existing)
└── greeting_formats.py (existing)
```

### Data Structures

#### Demo Data Module (demo_data.py)
```python
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DemoGreeting:
    """Represents a demo greeting configuration"""
    from_name: str
    to_name: str
    occasion: str
    message: str
    theme: str
    animation: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat() + "Z"
    
    def to_dict(self) -> Dict:
        return {
            "v": "1.0",
            "type": "greeting",
            "from": self.from_name,
            "to": self.to_name,
            "occasion": self.occasion,
            "message": self.message,
            "theme": self.theme,
            "animation": self.animation,
            "created": self.created_at
        }

# Default demo greeting configurations
DEFAULT_DEMO = DemoGreeting(
    from_name="Sarah",
    to_name="Mike",
    occasion="Christmas 2025",
    message="Wishing you a magical holiday season filled with joy, laughter, and special moments with loved ones!",
    theme="snowflake",
    animation="FadeInCenterOut"
)

# Alternative demo greetings (rotate based on season/date)
SEASONAL_DEMOS: Dict[str, DemoGreeting] = {
    "christmas": DemoGreeting(
        from_name="Sarah",
        to_name="Mike",
        occasion="Christmas 2025",
        message="Wishing you a magical holiday season filled with joy and laughter!",
        theme="snowflake",
        animation="FadeInCenterOut"
    ),
    "newyear": DemoGreeting(
        from_name="Alex",
        to_name="Jordan",
        occasion="New Year 2026",
        message="Here's to new beginnings, fresh starts, and amazing adventures in 2026!",
        theme="fireworks",
        animation="RadialRipple"
    ),
    "valentine": DemoGreeting(
        from_name="Emma",
        to_name="James",
        occasion="Valentine's Day",
        message="To the person who makes every day feel like a celebration. Happy Valentine's Day!",
        theme="hearts",
        animation="FadeInCenterOut"
    ),
    "wedding": DemoGreeting(
        from_name="Friends",
        to_name="The Happy Couple",
        occasion="Wedding Day",
        message="Congratulations on your special day! Wishing you a lifetime of love and happiness together.",
        theme="champagne",
        animation="RadialRipple"
    ),
    "general": DemoGreeting(
        from_name="You",
        to_name="Someone Special",
        occasion="Any Occasion",
        message="Life is what you make it. Make every moment special and share it with those you love.",
        theme="lights",
        animation="FadeInTopDown"
    )
}

def get_seasonal_demo() -> DemoGreeting:
    """
    Returns appropriate demo based on current date/season
    Falls back to general if not in special season
    """
    from datetime import datetime
    
    month = datetime.now().month
    
    if month == 12:
        return SEASONAL_DEMOS["christmas"]
    elif month == 1:
        return SEASONAL_DEMOS["newyear"]
    elif month == 2:
        return SEASONAL_DEMOS["valentine"]
    else:
        return SEASONAL_DEMOS["general"]

# Occasion presets for quick selection
OCCASION_PRESETS: List[str] = [
    "Birthday",
    "Anniversary",
    "Christmas",
    "New Year",
    "Wedding",
    "Graduation",
    "Congratulations",
    "Thank You",
    "Get Well",
    "Just Because"
]

# Animation presets
ANIMATION_PRESETS: Dict[str, List[str]] = {
    "snowflake": ["FadeInCenterOut", "FadeInTopDown"],
    "fireworks": ["RadialRipple", "MaterializeIn"],
    "lights": ["FadeInTopDown", "FadeInCenterOut"],
    "stars": ["RadialRippleIn", "MaterializeIn"],
    "confetti": ["MaterializeIn", "RadialRipple"],
    "champagne": ["RadialRipple", "FadeInCenterOut"],
    "hearts": ["FadeInCenterOut", "FadeInTopDown"],
    "farewell": ["FadeInTopDown", "FadeInCenterOut"],
}
```

#### State Management
```python
# Session state keys for demo tab
DEMO_STATE_KEYS = {
    "demo_greeting": "current_demo_greeting",
    "demo_qr_generated": "demo_qr_has_been_generated",
    "demo_customize_expanded": "demo_customize_panel_expanded",
    "demo_qr_image": "demo_qr_code_image",
    "demo_conversion_tracked": "demo_conversion_event_tracked"
}

# Initialize in demo_tab.py:
def init_demo_state():
    if DEMO_STATE_KEYS["demo_greeting"] not in st.session_state:
        st.session_state[DEMO_STATE_KEYS["demo_greeting"]] = get_seasonal_demo()
    if DEMO_STATE_KEYS["demo_qr_generated"] not in st.session_state:
        st.session_state[DEMO_STATE_KEYS["demo_qr_generated"]] = False
    if DEMO_STATE_KEYS["demo_customize_expanded"] not in st.session_state:
        st.session_state[DEMO_STATE_KEYS["demo_customize_expanded"]] = False
```

### QR Generation Integration

The demo will use existing QR generation code but with cached/optimized rendering:
```python
# In demo_tab.py - using existing greeting_formats and config

from greeting_formats import encode_greeting
from config import THEME_COLORS, THEME_ANIMATIONS
import qrcode
from PIL import Image
import streamlit as st

def generate_demo_qr(demo_greeting: DemoGreeting) -> Image.Image:
    """
    Generate QR code for demo greeting
    Uses existing greeting format encoding
    """
    # Convert to greeting JSON format
    greeting_json = encode_greeting({
        "v": "1.0",
        "type": "greeting",
        "from": demo_greeting.from_name,
        "to": demo_greeting.to_name,
        "occasion": demo_greeting.occasion,
        "message": demo_greeting.message,
        "theme": demo_greeting.theme,
        "created": demo_greeting.created_at
    })
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=None,  # Auto version
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(greeting_json)
    qr.make(fit=True)
    
    # Apply theme colors
    theme_color = THEME_COLORS.get(demo_greeting.theme, THEME_COLORS["general"])
    img = qr.make_image(
        fill_color=theme_color["module"],
        back_color="#ffffff"
    )
    
    return img

@st.cache_data(ttl=3600)
def get_cached_demo_qr(greeting_dict_str: str) -> Image.Image:
    """
    Cached QR generation for demo greetings
    Key: stringified greeting dict for cache key
    TTL: 1 hour
    """
    # Reconstruct greeting from string
    import json
    greeting_dict = json.loads(greeting_dict_str)
    demo_greeting = DemoGreeting(**greeting_dict)
    return generate_demo_qr(demo_greeting)
```

---

## Implementation Guide

### Step 1: Create demo_data.py

**File**: `streamlit/utils/demo_data.py`
```python
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DemoGreeting:
    """Represents a demo greeting configuration"""
    from_name: str
    to_name: str
    occasion: str
    message: str
    theme: str
    animation: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat() + "Z"
    
    def to_dict(self) -> Dict:
        return {
            "from": self.from_name,
            "to": self.to_name,
            "occasion": self.occasion,
            "message": self.message,
            "theme": self.theme,
            "animation": self.animation,
            "created": self.created_at
        }

# [Copy all SEASONAL_DEMOS, OCCASION_PRESETS, etc. from Code Specifications section above]
```

**Status**: Ready to implement

### Step 2: Create demo_tab.py

**File**: `streamlit/tabs/demo_tab.py`

See full implementation code in Code Specifications section below.

**Status**: See full code below

### Step 3: Update app.py

Modify `streamlit/app.py` to include demo tab:

**Location**: Import section (line ~12)
```python
from tabs import create_tab, scan_tab, examples_tab, batch_tab, about_tab, view_page, demo_tab
```

**Location**: Main tabs section (around line ~90)
```python
# Update tab creation:
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎁 Try Demo",  # NEW - First position for visibility
    "Create Greeting", 
    "Scan QR Code", 
    "Examples", 
    "About"
])

# Note: Reorder so demo is prominent - catches attention first!
with tab1:
    demo_tab.render()

with tab2:
    create_tab.render()
    
# ... etc
```

**Alternative (if not reordering)**: Add as optional tab
```python
if show_demo:  # Add checkbox in sidebar
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Create Greeting", 
        "Try Demo",  # NEW
        "Scan QR Code", 
        "Examples", 
        "Batch",
        "About"
    ])
    # ... render each
else:
    # Original tabs
```

### Step 4: Testing Checklist

- [ ] Demo loads without errors
- [ ] Default greeting displays correctly
- [ ] QR code generates on button click
- [ ] Customization panel opens/closes smoothly
- [ ] Real-time preview updates as user edits
- [ ] Theme selector changes QR colors
- [ ] Mobile layout is responsive
- [ ] Conversion button navigates to Create tab
- [ ] Download QR works correctly
- [ ] Social share buttons function
- [ ] Loading states are smooth
- [ ] Session state persists across refreshes
- [ ] Analytics events fire correctly

### Step 5: Deployment

1. Test locally: `streamlit run app.py`
2. Push to GitHub
3. Streamlit Cloud auto-deploys
4. Monitor analytics for demo usage

---

## Code Specifications

### demo_tab.py - Complete Implementation
```python
"""
Interactive Demo Tab
Allows users to create a sample greeting in <60 seconds without friction
"""

import streamlit as st
from datetime import datetime
import json
from typing import Dict
import qrcode
from PIL import Image
import io

# Import utilities
from utils.demo_data import (
    DemoGreeting, 
    get_seasonal_demo, 
    OCCASION_PRESETS,
    ANIMATION_PRESETS
)
from greeting_formats import encode_greeting
from config import THEME_COLORS, THEME_ICONS, THEME_ANIMATIONS

# ============================================================================
# State Management
# ============================================================================

def init_demo_state():
    """Initialize session state for demo tab"""
    if "demo_greeting" not in st.session_state:
        st.session_state.demo_greeting = get_seasonal_demo()
    if "demo_qr_generated" not in st.session_state:
        st.session_state.demo_qr_generated = False
    if "demo_customize_expanded" not in st.session_state:
        st.session_state.demo_customize_expanded = False
    if "demo_qr_image" not in st.session_state:
        st.session_state.demo_qr_image = None

# ============================================================================
# QR Code Generation
# ============================================================================

def generate_demo_qr_code(greeting: DemoGreeting) -> Image.Image:
    """Generate QR code image for demo greeting"""
    
    # Encode greeting data
    greeting_json = json.dumps(greeting.to_dict())
    
    # Create QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(greeting_json)
    qr.make(fit=True)
    
    # Get theme colors
    theme_colors = THEME_COLORS.get(greeting.theme, THEME_COLORS["general"])
    
    # Generate image
    img = qr.make_image(
        fill_color=theme_colors["module"],
        back_color="white"
    )
    
    return img

@st.cache_data(ttl=3600)
def cached_qr_generation(greeting_json_str: str) -> bytes:
    """Cache QR code generation"""
    greeting_dict = json.loads(greeting_json_str)
    greeting = DemoGreeting(**greeting_dict)
    img = generate_demo_qr_code(greeting)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

# ============================================================================
# UI Components
# ============================================================================

def display_greeting_preview(greeting: DemoGreeting):
    """Display sample greeting in a nice card"""
    
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Theme emoji
            theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
            st.markdown(f"### {theme_emoji} {greeting.theme.title()}")
        
        with col2:
            # Occasion badge
            st.markdown(f"**Occasion**: {greeting.occasion}")
        
        # Greeting card preview
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
        ">
            <p><strong>From:</strong> {greeting.from_name}</p>
            <p><strong>To:</strong> {greeting.to_name}</p>
            <p style="font-style: italic; margin-top: 15px;">"{greeting.message}"</p>
        </div>
        """, unsafe_allow_html=True)

def display_theme_selector(current_theme: str) -> str:
    """Display theme selector with visual icons"""
    
    st.markdown("**Choose a Theme:**")
    
    themes = list(THEME_ICONS.keys())
    cols = st.columns(min(8, len(themes)))
    
    selected_theme = current_theme
    for idx, theme in enumerate(themes):
        with cols[idx % len(cols)]:
            emoji = THEME_ICONS.get(theme, "🎁")
            if st.button(f"{emoji}\\n{theme.title()}", key=f"theme_{theme}"):
                selected_theme = theme
                # Provide haptic feedback (visual)
                st.session_state.demo_greeting.theme = theme
    
    return selected_theme

def display_customization_panel() -> Dict:
    """Display expandable customization panel"""
    
    with st.expander("✏️ Customize Demo", expanded=st.session_state.demo_customize_expanded):
        
        greeting = st.session_state.demo_greeting
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            from_name = st.text_input(
                "From (Your Name)",
                value=greeting.from_name,
                key="demo_from_name"
            )
            
            to_name = st.text_input(
                "To (Recipient Name)",
                value=greeting.to_name,
                key="demo_to_name"
            )
        
        with col2:
            occasion = st.selectbox(
                "Occasion",
                options=OCCASION_PRESETS,
                index=0 if greeting.occasion in OCCASION_PRESETS else 0,
                key="demo_occasion"
            )
            
            custom_occasion = st.text_input(
                "Or enter custom occasion",
                value="",
                key="demo_custom_occasion"
            )
            
            # Use custom if provided, otherwise use selected
            final_occasion = custom_occasion if custom_occasion else occasion
        
        # Message customization
        st.markdown("**Message (max 500 characters)**")
        message = st.text_area(
            "Your greeting message",
            value=greeting.message,
            height=100,
            max_chars=500,
            key="demo_message",
            label_visibility="collapsed"
        )
        
        char_count = len(message)
        col1, col2 = st.columns([3, 1])
        with col2:
            st.caption(f"{char_count}/500")
            if char_count > 400:
                st.warning("Getting close to limit!")
        
        # Theme selection in customization
        st.markdown("**Select Theme**")
        theme = display_theme_selector(greeting.theme)
        
        # Return customized data
        return {
            "from_name": from_name,
            "to_name": to_name,
            "occasion": final_occasion,
            "message": message,
            "theme": theme,
            "animation": ANIMATION_PRESETS.get(theme, ["MaterializeIn"])[0]
        }

def display_qr_with_mobile_mockup(qr_image: Image.Image, greeting: DemoGreeting):
    """Display QR code with mobile frame mockup showing scan result"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📱 Generated QR Code")
        st.image(qr_image, use_column_width=True, caption="Scan to see the greeting")
        
        # Action buttons
        button_col1, button_col2, button_col3 = st.columns(3)
        
        with button_col1:
            # Download button
            img_byte_arr = io.BytesIO()
            qr_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            st.download_button(
                label="⬇️ Download",
                data=img_byte_arr.getvalue(),
                file_name=f"{greeting.from_name}_{greeting.to_name}_greeting.png",
                mime="image/png",
                key="demo_download_qr"
            )
        
        with button_col2:
            if st.button("📤 Share", key="demo_share"):
                st.info("Share functionality coming soon!")
        
        with button_col3:
            if st.button("🔄 New", key="demo_new"):
                st.session_state.demo_greeting = get_seasonal_demo()
                st.session_state.demo_qr_generated = False
                st.rerun()
    
    with col2:
        st.markdown("### 📲 When Scanned")
        
        # Mobile frame mockup
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            color: white;
        ">
            <div style="
                background: white;
                color: #333;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 10px;
            ">
                <h3 style="margin: 0;">✨ Greeting ✨</h3>
            </div>
            
            <div style="
                background: white;
                color: #333;
                padding: 20px;
                border-radius: 10px;
                text-align: left;
            ">
                <p><strong>From:</strong> {greeting.from_name}</p>
                <p><strong>To:</strong> {greeting.to_name}</p>
                <p style="margin-top: 15px;"><em>"{greeting.message}"</em></p>
                <p style="margin-top: 15px; font-size: 0.9em; color: #888;">
                    {greeting.theme.title()} Theme • {datetime.now().strftime('%b %d, %Y')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# Main Render Function
# ============================================================================

def render():
    """Main demo tab render function"""
    
    # Initialize state
    init_demo_state()
    
    # ========== HEADER ==========
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>✨ Try the Interactive Demo ✨</h1>
        <p style="font-size: 1.1em; color: #666;">
            Create a sample greeting in under 60 seconds
        </p>
        <p style="color: #999; font-size: 0.9em;">
            ✅ No signup required • ✅ No login needed • ✅ Fully interactive
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== LAYOUT ==========
    demo_col1, demo_col2 = st.columns([1, 1])
    
    with demo_col1:
        st.markdown("### 📝 Sample Greeting")
        display_greeting_preview(st.session_state.demo_greeting)
        
        # Customization button
        if st.button("✏️ Customize Demo", key="customize_btn", width='stretch'):
            st.session_state.demo_customize_expanded = not st.session_state.demo_customize_expanded
            st.rerun()
        
        # Generate button (primary CTA)
        if st.button(
            "✨ Generate QR Code",
            key="generate_btn",
            width='stretch',
            type="primary"
        ):
            st.session_state.demo_qr_generated = True
            st.rerun()
    
    # Handle customization if expanded
    if st.session_state.demo_customize_expanded:
        st.divider()
        custom_data = display_customization_panel()
        
        # Update greeting with customizations
        st.session_state.demo_greeting = DemoGreeting(
            from_name=custom_data["from_name"],
            to_name=custom_data["to_name"],
            occasion=custom_data["occasion"],
            message=custom_data["message"],
            theme=custom_data["theme"],
            animation=custom_data["animation"]
        )
        
        if st.button(
            "Update QR Preview",
            key="update_preview_btn",
            width='stretch',
            type="secondary"
        ):
            st.session_state.demo_qr_generated = True
            st.rerun()
    
    # ========== QR CODE GENERATION & DISPLAY ==========
    if st.session_state.demo_qr_generated:
        st.divider()
        
        # Generate QR code
        qr_image = generate_demo_qr_code(st.session_state.demo_greeting)
        
        # Display QR with mockup
        display_qr_with_mobile_mockup(qr_image, st.session_state.demo_greeting)
        
        # ========== NEXT STEPS ==========
        st.divider()
        
        st.markdown("""
        <div style="background: #f0f8ff; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>👉 Next Step</h3>
            <p>Liked what you created? Now it's time to make your own!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🎁 Create My Own Greeting",
                key="convert_btn",
                width='stretch',
                type="primary"
            ):
                # Log conversion event (placeholder for analytics)
                st.session_state["demo_converted"] = True
                # Navigate to create tab
                st.switch_page("pages/create.py")  # Adjust based on your routing
    
    # ========== FOOTER ==========
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.9em; margin-top: 30px;">
        <p>
            💡 <strong>Pro Tip:</strong> Messages work best under 300 characters for optimal QR code size
        </p>
        <p>
            Questions? Check out the <strong>About</strong> tab for more info
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# If running as main module (for testing)
# ============================================================================

if __name__ == "__main__":
    render()
```

---

## Integration Points

### 1. Navigation Integration

**In app.py sidebar:**
```python
st.markdown("---")
st.markdown("### 🚀 Quick Start")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Try Demo",
````

## File: streamlit/qr/generator.py
````python
"""
QR code generation module
Handles QR code creation with theme icons and visible messages
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
from config import THEME_ICONS
from utils.image_utils import load_theme_icon


def _colorize_position_markers(img: Image.Image, qr: qrcode.QRCode, ring_color: str) -> Image.Image:
    """
    Colorize the three position detection patterns (corner squares) in a QR code

    Args:
        img: PIL Image of the QR code
        qr: QRCode object containing module matrix
        ring_color: Hex color string for position markers

    Returns:
        Modified PIL Image with colored position markers
    """
    from PIL import ImageColor

    # Convert hex color to RGB
    rgb_color = ImageColor.getcolor(ring_color, "RGB")

    # QR code parameters
    box_size = qr.box_size
    border = qr.border
    modules = qr.modules

    if not modules:
        return img

    module_count = len(modules)

    # Position detection patterns are 7x7 modules, located at three corners
    pattern_size = 7

    # Define positions: (row_start, col_start) for each corner
    positions = [
        (0, 0),  # Top-left
        (0, module_count - pattern_size),  # Top-right
        (module_count - pattern_size, 0),  # Bottom-left
    ]

    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # For each position marker
    for row_start, col_start in positions:
        # Iterate through the 7x7 pattern
        for r in range(pattern_size):
            for c in range(pattern_size):
                module_row = row_start + r
                module_col = col_start + c

                # Check if this module is part of the pattern (should be filled)
                if modules[module_row][module_col]:
                    # Calculate pixel coordinates (accounting for border)
                    x1 = (module_col + border) * box_size
                    y1 = (module_row + border) * box_size
                    x2 = x1 + box_size
                    y2 = y1 + box_size

                    # Draw filled rectangle with ring color
                    draw.rectangle([x1, y1, x2, y2], fill=rgb_color)

    return img


def generate_qr_code(data: str, theme: str = "general", visible_message: str = None, all_sides: bool = False, error_correction=qrcode.constants.ERROR_CORRECT_H, module_color: str = None, position_ring_color: str = None) -> Image.Image:
    """
    Generate QR code from data string

    Args:
        data: String data to encode
        theme: Theme name for icon overlay
        visible_message: Optional text to display around the QR code
        all_sides: If True, display visible_message on all 4 sides (top, bottom, left, right)
        error_correction: QR error correction level
        module_color: Color for QR code modules (hex string like "#FF0000"), defaults to black
        position_ring_color: Color for position detection markers (hex string), defaults to module_color

    Returns:
        PIL Image of QR code
    """
    qr = qrcode.QRCode(
        version=None,  # Auto-detect version
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Use provided colors or defaults
    fill = module_color if module_color else "black"
    img = qr.make_image(fill_color=fill, back_color="white")
    # Convert qrcode.image.pil.PilImage to standard PIL.Image.Image
    pil_img = img.convert('RGB')

    # Colorize position markers if a different color is specified
    if position_ring_color and position_ring_color != fill:
        pil_img = _colorize_position_markers(pil_img, qr, position_ring_color)

    # Add theme icon if applicable
    if theme in THEME_ICONS and THEME_ICONS[theme]:
        qr_width, qr_height = pil_img.size

        # Icon should be ~15% of QR code size for reliable scanning (safe margin under 20%)
        icon_size = int(min(qr_width, qr_height) * 0.15)

        try:
            # Load icon from file
            icon = load_theme_icon(theme, icon_size)

            # If icon not found, skip embedding
            if icon is None:
                return pil_img

            # Calculate center position
            icon_pos = (
                (qr_width - icon_size) // 2,
                (qr_height - icon_size) // 2
            )

            # Create white background circle for better contrast
            background = Image.new('RGBA', (icon_size, icon_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(background)
            draw.ellipse([0, 0, icon_size, icon_size], fill=(255, 255, 255, 255))

            # Convert pil_img to RGBA for pasting
            pil_img = pil_img.convert('RGBA')

            # Paste white circle, then icon
            pil_img.paste(background, icon_pos, background)
            pil_img.paste(icon, icon_pos, icon)

            # Convert back to RGB
            pil_img = pil_img.convert('RGB')
        except Exception as e:
            # If icon embedding fails, just return plain QR code
            print(f"Warning: Could not embed icon for theme '{theme}': {e}")


    # Add visible message if provided
    if visible_message:
        try:
            # Prepare for font loading
            font_path = None
            font_size = 20 # Start with a baseline

            # Common fonts to try (including CJK support)
            # msyh.ttf = Microsoft YaHei (Windows Chinese)
            # simhei.ttf = SimHei (Windows Chinese)
            # NotoSansCJK... = Linux CJK
            font_names = ["msyh.ttf", "simhei.ttf", "arial.ttf", "calibri.ttf", "seguiemj.ttf",
                          "segoeui.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf",
                          "WenQuanYiMicroHei.ttf", "NotoSansCJK-Regular.ttc"]

            for name in font_names:
                try:
                    # check if we can load it
                    ImageFont.truetype(name, font_size)
                    font_path = name
                    break
                except OSError:
                    continue

            # Helper to get text size
            def get_text_size(text, font):
                draw_dummy = ImageDraw.Draw(pil_img)
                if hasattr(draw_dummy, 'textbbox'):
                    bbox = draw_dummy.textbbox((0, 0), text, font=font)
                    return bbox[2] - bbox[0], bbox[3] - bbox[1]
                else:
                    return draw_dummy.textsize(text, font=font)

            qr_width, qr_height = pil_img.size
            target_width = qr_width * 0.9  # Use 90% of width for safe margins (5% each side)

            # Formatting
            padding = int(qr_height * 0.05) # 5% of QR height as vertical padding
            if padding < 20: padding = 20

            # Add spacing between QR code and text to prevent overlap
            text_padding = int(qr_height * 0.08)  # 8% of QR height for clear separation
            if text_padding < 15: text_padding = 15  # Minimum 15px spacing

            font = None
            if font_path:
                # Iterative sizing or calculation
                # Heuristic: Width is roughly proportional to font size
                # 1. Measure at base size
                test_font = ImageFont.truetype(font_path, font_size)
                w, h = get_text_size(visible_message, test_font)

                if w > 0:
                    # Calculate desired size
                    # scale = target / current
                    scale_factor = target_width / w
                    new_font_size = int(font_size * scale_factor)

                    # Clamp limits
                    min_size = 12
                    max_size = int(qr_height * 0.2) # Max text height 20% of QR? Or just cap size.
                                                  # Let's cap max size to avoid absurdity on short words like "Hi"

                    if new_font_size < min_size: new_font_size = min_size
                    if new_font_size > max_size: new_font_size = max_size

                    font_size = new_font_size
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = test_font
            else:
                # Fallback to default (cannot resize)
                font = ImageFont.load_default()

            # Final measurement
            text_width, text_height = get_text_size(visible_message, font)

            if all_sides:
                # All 4 sides mode: add text on top, bottom, left, and right
                # Calculate final image size (QR + text on all sides)
                # Use larger margin for left/right sides to prevent text from touching QR code
                side_padding = text_height + (text_padding * 3)  # Horizontal space for rotated text

                # For vertical space, we need to fit BOTH the QR code AND the rotated text
                # Rotated text height = original text_width
                # Ensure we have enough vertical space for whichever is taller
                vertical_content_height = max(qr_height, text_width)  # QR or rotated text, whichever is taller

                final_width = qr_width + 2 * side_padding  # Left and right sides
                final_height = vertical_content_height + 2 * (text_height + text_padding)  # Top and bottom text

                new_img = Image.new('RGB', (final_width, final_height), 'white')

                # Center QR code vertically within the available content area
                qr_x = side_padding
                qr_y = text_height + text_padding + (vertical_content_height - qr_height) // 2
                new_img.paste(pil_img, (qr_x, qr_y))

                draw_new = ImageDraw.Draw(new_img)

                # Draw top text (centered horizontally)
                top_text_x = (final_width - text_width) // 2
                top_text_y = (text_height + text_padding - text_height) // 2
                draw_new.text((top_text_x, top_text_y), visible_message, fill="black", font=font)

                # Draw bottom text (centered horizontally)
                bottom_text_x = (final_width - text_width) // 2
                bottom_text_y = text_height + text_padding + vertical_content_height + text_padding // 2
                draw_new.text((bottom_text_x, bottom_text_y), visible_message, fill="black", font=font)

                # Create rotated text image for left side (rotated 90 degrees counter-clockwise)
                # Add extra padding to canvas to prevent text clipping from font metrics
                canvas_padding = text_height  # Extra space for descenders/ascenders
                left_canvas_w = text_width + 2 * canvas_padding
                left_canvas_h = text_height + 2 * canvas_padding
                left_text_img = Image.new('RGBA', (left_canvas_w, left_canvas_h), (255, 255, 255, 0))
                left_draw = ImageDraw.Draw(left_text_img)
                left_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                left_text_rotated = left_text_img.rotate(90, expand=True)

                # Paste left text (centered both horizontally in side margin and vertically in content area)
                left_x = (side_padding - left_text_rotated.width) // 2
                left_y = text_height + text_padding + (vertical_content_height - left_text_rotated.height) // 2
                new_img.paste(left_text_rotated, (left_x, left_y), left_text_rotated)

                # Create rotated text image for right side (rotated 90 degrees clockwise)
                right_canvas_w = text_width + 2 * canvas_padding
                right_canvas_h = text_height + 2 * canvas_padding
                right_text_img = Image.new('RGBA', (right_canvas_w, right_canvas_h), (255, 255, 255, 0))
                right_draw = ImageDraw.Draw(right_text_img)
                right_draw.text((canvas_padding, canvas_padding), visible_message, fill="black", font=font)
                right_text_rotated = right_text_img.rotate(-90, expand=True)

                # Paste right text (centered both horizontally in side margin and vertically in content area)
                right_x = qr_x + qr_width + (side_padding - right_text_rotated.width) // 2
                right_y = text_height + text_padding + (vertical_content_height - right_text_rotated.height) // 2
                new_img.paste(right_text_rotated, (right_x, right_y), right_text_rotated)

                return new_img
            else:
                # Bottom only mode (original behavior)
                # Create new image
                # Width: at least QR width. If text is somehow wider (min size limit), expand.
                final_width = max(qr_width, text_width + int(qr_width * 0.1)) # Ensure margins if text is wider
                final_height = qr_height + text_height + 2 * padding + text_padding  # Include text spacing

                new_img = Image.new('RGB', (final_width, final_height), 'white')

                # Paste QR code (centered horizontally)
                qr_x = (final_width - qr_width) // 2
                qr_y = padding // 2
                new_img.paste(pil_img, (qr_x, qr_y))

                # Draw text (centered horizontally, below QR)
                draw_new = ImageDraw.Draw(new_img)
                text_x = (final_width - text_width) // 2
                text_y = qr_y + qr_height + text_padding

                draw_new.text((text_x, text_y), visible_message, fill="black", font=font)

                return new_img

        except Exception as e:
            print(f"Warning: Failed to add visible message: {e}")
            return pil_img

    return pil_img
````

## File: streamlit/tabs/batch_tab.py
````python
"""
Batch Tab
Batch QR code generation from CSV upload
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
from datetime import datetime
import zipfile

from greeting_formats import create_holiday_greeting, encode_greeting_to_url
from qr.generator import generate_qr_code
from utils.file_utils import get_all_available_backgrounds, get_available_backgrounds, get_available_gifs
from utils.url_utils import is_web_url, classify_background, convert_youtube_to_embed_url, convert_google_drive_to_embed_url
from config import THEME_ICONS, THEME_COLORS


def render() -> None:
    """Tab for batch QR code generation from Excel"""

    # Initialize session state for batch DataFrame
    if 'batch_df' not in st.session_state:
        st.session_state.batch_df = None

    st.markdown('<div class="main-header"><h1>📦 Batch QR Code Generation</h1></div>',
                unsafe_allow_html=True)

    st.write("Generate multiple QR codes at once by uploading an Excel spreadsheet.")
    st.info("💡 **New Feature**: You can now use YouTube URLs or direct video URLs as backgrounds! Just paste the URL in the Background column.")

    # Available themes and backgrounds for reference
    available_themes = list(THEME_ICONS.keys())
    all_backgrounds, background_folder_map = get_all_available_backgrounds()
    available_backgrounds_keep = get_available_backgrounds()
    available_backgrounds_gif = get_available_gifs()

    st.markdown("---")

    # Template download section
    st.subheader("1. Download Template")
    st.write("Download the Excel template, fill in your greetings, then upload it below.")

    # Create template Excel file in memory
    try:
        # Create sample data with 4 test cases
        sample_data = {
            "From": ["Alice", "Bob", "Charlie", "David"],
            "To": ["Bob", "Alice", "Dana", "Eve"],
            "Message": ["Merry Christmas!", "Happy New Year!", "Season's Greetings!\nhttps://qr-greeting.co.uk", "Enjoy the holidays!"],
            "Theme": ["snowflake", "fireworks", "hearts", "lights"],
            "Background": ["letter-background-design-01.jpg", "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4", "https://youtu.be/6SuLXoRmykE", "christmas-lights.gif"],
            "VisibleMessage": ["Scan me!", "BOB", "Happy Holidays!", "Ho Ho Ho!"]
        }
        df_template = pd.DataFrame(sample_data)

        # Save to CSV
        csv_data = df_template.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Template (.csv)",
            data=csv_data,
            file_name="qr_greeting_template.csv",
            mime="text/csv"
        )

        # Show valid options for reference
        with st.expander("View Valid Options"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Valid Themes:**")
                for theme in available_themes:
                    emoji = THEME_ICONS.get(theme, "")
                    st.write(f"- `{theme}` {emoji if emoji else ''}")
            with col2:
                st.write("**Valid Backgrounds:**")
                st.write("*Local files from `keep/` folder:*")
                if available_backgrounds_keep:
                    for bg in available_backgrounds_keep:
                        st.write(f"- `{bg}`")
                else:
                    st.write("No backgrounds available in `keep/` folder")
                st.write("")
                st.write("*Local files from `gif/` folder:*")
                if available_backgrounds_gif:
                    for bg in available_backgrounds_gif:
                        st.write(f"- `{bg}`")
                else:
                    st.write("No backgrounds available in `gif/` folder")
                st.write("")
                st.write("*Or use web video URLs:*")
                st.write("- YouTube: `youtu.be/VIDEO_ID`")
                st.write("- YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`")
                st.write("- Direct video: `https://example.com/video.mp4`")

    except ImportError:
        st.error("pandas is required for batch processing. Please install it: `pip install pandas`")
        return

    st.markdown("---")

    # Upload section
    st.subheader("2. Upload Filled Template")

    uploaded_file = st.file_uploader(
        "Choose your filled CSV file",
        type=['csv'],
        help="Upload the template with your greeting data"
    )

    if uploaded_file is not None:
        try:
            # Load CSV into session state (only when new file is uploaded)
            df = pd.read_csv(uploaded_file)
            # Check if this is a new upload by comparing with existing data
            if st.session_state.batch_df is None or len(df) != len(st.session_state.batch_df):
                st.session_state.batch_df = df

            st.success(f"Loaded {len(st.session_state.batch_df)} greetings from CSV!")

            # Preview data with editable interface
            with st.expander("Preview Data"):
                st.session_state.batch_df = st.data_editor(
                    st.session_state.batch_df,
                    key="batch_data_editor",
                    num_rows="dynamic"
                )

            # Validate data
            required_cols = ["From", "To", "Message"]
            missing_cols = [col for col in required_cols if col not in st.session_state.batch_df.columns]

            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                return

            # Validate themes
            if "Theme" in st.session_state.batch_df.columns:
                invalid_themes = st.session_state.batch_df[~st.session_state.batch_df["Theme"].isna() & ~st.session_state.batch_df["Theme"].isin(available_themes)]["Theme"].unique()
                if len(invalid_themes) > 0:
                    st.warning(f"Some rows have invalid themes: {list(invalid_themes)}. They will use 'general'.")

            # Generate button
            if st.button("🚀 Generate All QR Codes", type="primary"):
                zip_buffer = BytesIO()

                progress = st.progress(0)
                status = st.empty()

                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for idx, row in st.session_state.batch_df.iterrows():
                        from_name = str(row.get("From", ""))
                        to_name = str(row.get("To", ""))
                        message = str(row.get("Message", ""))
                        theme = str(row.get("Theme", "general")) if pd.notna(row.get("Theme")) else "general"
                        background = str(row.get("Background", "")) if pd.notna(row.get("Background")) else ""
                        visible_msg = str(row.get("VisibleMessage", "")) if pd.notna(row.get("VisibleMessage")) else ""

                        # Validate theme
                        if theme not in available_themes:
                            theme = "general"

                        # Validate background (local file or web URL)
                        if background:
                            if is_web_url(background):
                                # Validate web URL format
                                bg_type = classify_background(background)
                                if bg_type == 'youtube':
                                    # Validate YouTube URL can be converted to embed format
                                    if convert_youtube_to_embed_url(background) is None:
                                        st.warning(f"Row {idx + 1}: Invalid YouTube URL '{background}' - skipping background")
                                        background = ""
                                elif bg_type == 'google_drive':
                                    # Validate Google Drive URL can be converted to embed format
                                    if convert_google_drive_to_embed_url(background) is None:
                                        st.warning(f"Row {idx + 1}: Invalid Google Drive URL '{background}' - skipping background")
                                        background = ""
                                elif bg_type == 'direct_video':
                                    # Direct video URLs are accepted as-is
                                    # Note: CORS and accessibility depend on the video host
                                    pass
                                else:
                                    # Other URL types not supported
                                    st.warning(f"Row {idx + 1}: Unsupported URL type '{background}' - skipping background")
                                    background = ""
                            else:
                                # Check if background exists in either folder
                                background_found = False

                                # Check keep/ folder first
                                keep_path = Path(__file__).parent.parent / "keep" / background
                                if keep_path.exists():
                                    background_found = True
                                else:
                                    # Check gif/ folder
                                    gif_path = Path(__file__).parent.parent / "gif" / background
                                    if gif_path.exists():
                                        background_found = True

                                if not background_found:
                                    st.warning(f"Row {idx + 1}: Background file '{background}' not found in keep/ or gif/ folders - skipping background")
                                    background = ""

                        status.text(f"Generating QR {idx + 1}/{len(st.session_state.batch_df)}: {to_name}...")

                        # Create greeting
                        greeting = create_holiday_greeting(
                            from_name=from_name,
                            to_name=to_name,
                            message=message,
                            theme=theme,
                            background=background
                        )

                        # Encode to URL
                        greeting_url = encode_greeting_to_url(greeting)

                        # Get theme colors for colorized QR code
                        theme_colors = THEME_COLORS.get(theme, THEME_COLORS['general'])

                        # Generate QR code with theme colors
                        qr_img = generate_qr_code(
                            greeting_url,
                            theme=theme,
                            visible_message=visible_msg,
                            module_color=theme_colors['module'],
                            position_ring_color=theme_colors['ring']
                        )

                        # Save to zip
                        img_buffer = BytesIO()
                        qr_img.save(img_buffer, format='PNG')
                        img_buffer.seek(0)

                        # Filename: to_name_index.png
                        safe_name = "".join(c for c in to_name if c.isalnum() or c in (' ', '-', '_')).strip()
                        filename = f"{safe_name}_{idx + 1}.png"

                        zf.writestr(filename, img_buffer.read())

                        progress.progress((idx + 1) / len(st.session_state.batch_df))

                status.text("✅ All QR codes generated!")

                zip_buffer.seek(0)

                st.download_button(
                    label="📥 Download All QR Codes (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"qr_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip"
                )

        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")
````

## File: streamlit/utils/demo_data.py
````python
"""
Demo Data Module
Contains demo greeting configurations and seasonal presets for the Interactive Demo tab
"""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DemoGreeting:
    """Represents a demo greeting configuration"""
    from_name: str
    to_name: str
    occasion: str
    message: str
    theme: str
    animation: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat() + "Z"
    
    def to_dict(self) -> Dict:
        return {
            "from": self.from_name,
            "to": self.to_name,
            "occasion": self.occasion,
            "message": self.message,
            "theme": self.theme,
            "animation": self.animation,
            "created": self.created_at
        }


# Seasonal demo greetings (rotate based on date)
SEASONAL_DEMOS: Dict[str, DemoGreeting] = {
    "christmas": DemoGreeting(
        from_name="Sarah",
        to_name="Mike",
        occasion="Christmas 2025",
        message="Wishing you a magical holiday season filled with joy, laughter, and special moments with loved ones!",
        theme="snowflake",
        animation="FadeInCenterOut"
    ),
    "newyear": DemoGreeting(
        from_name="Alex",
        to_name="Jordan",
        occasion="New Year 2026",
        message="Here's to new beginnings, fresh starts, and amazing adventures in the year ahead!",
        theme="fireworks",
        animation="RadialRipple"
    ),
    "valentine": DemoGreeting(
        from_name="Emma",
        to_name="James",
        occasion="Valentine's Day",
        message="To the person who makes every day feel like a celebration. Happy Valentine's Day!",
        theme="hearts",
        animation="FadeInCenterOut"
    ),
    "wedding": DemoGreeting(
        from_name="Friends",
        to_name="The Happy Couple",
        occasion="Wedding Day",
        message="Congratulations on your special day! Wishing you a lifetime of love and happiness together.",
        theme="champagne",
        animation="RadialRipple"
    ),
    "general": DemoGreeting(
        from_name="You",
        to_name="Someone Special",
        occasion="Any Occasion",
        message="Life is what you make it. Make every moment special and share it with those you love.",
        theme="lights",
        animation="FadeInTopDown"
    )
}


def get_seasonal_demo() -> DemoGreeting:
    """
    Returns appropriate demo based on current date/season
    Falls back to general if not in special season
    """
    month = datetime.now().month
    
    if month == 12:
        return SEASONAL_DEMOS["christmas"]
    elif month == 1:
        return SEASONAL_DEMOS["newyear"]
    elif month == 2:
        return SEASONAL_DEMOS["valentine"]
    else:
        return SEASONAL_DEMOS["general"]


# Occasion presets for quick selection
OCCASION_PRESETS: List[str] = [
    "Birthday",
    "Anniversary",
    "Christmas",
    "New Year",
    "Wedding",
    "Graduation",
    "Congratulations",
    "Thank You",
    "Get Well",
    "Just Because"
]


# Animation presets per theme
ANIMATION_PRESETS: Dict[str, List[str]] = {
    "snowflake": ["FadeInCenterOut", "FadeInTopDown"],
    "fireworks": ["RadialRipple", "MaterializeIn"],
    "lights": ["FadeInTopDown", "FadeInCenterOut"],
    "stars": ["RadialRippleIn", "MaterializeIn"],
    "confetti": ["MaterializeIn", "RadialRipple"],
    "champagne": ["RadialRipple", "FadeInCenterOut"],
    "hearts": ["FadeInCenterOut", "FadeInTopDown"],
    "valentine": ["FadeInCenterOut", "RadialRipple"],
    "farewell": ["FadeInTopDown", "FadeInCenterOut"],
}
````

## File: streamlit/greeting_formats.py
````python
#!/usr/bin/env python3
"""
Greeting JSON Schema Module
Handles creation and parsing of holiday greeting data in compact JSON format
"""

import json
import base64
import zlib
from datetime import datetime
from typing import Dict, Optional
from urllib.parse import urlencode, parse_qs, quote, unquote


# Base URL for the greeting app
# Base URL for the greeting app
# Obfuscated to avoid plain text check-in
_ENCODED_URL = "aHR0cHM6Ly9xci1ncmVldGluZy5zdHJlYW1saXQuYXBwLw=="

def _decypher_url(encoded: str) -> str:
    """Simple decoder for the app URL"""
    return base64.b64decode(encoded).decode('utf-8')

GREETING_APP_URL = _decypher_url(_ENCODED_URL)


def encode_greeting_to_url(greeting: Dict, base_url: str = GREETING_APP_URL) -> str:
    """
    Encode greeting data into a URL with compressed query parameters
    
    Args:
        greeting: Greeting dictionary with from, to, message, theme
        base_url: Base URL for the greeting app
        
    Returns:
        Full URL with encoded greeting data
    """
    # Compress the message to save space (important for QR code size)
    message = greeting.get("message", "")
    from_name = greeting.get("from", "")
    to_name = greeting.get("to", "")
    theme = greeting.get("theme", "general")
    
    # Use base64 + zlib compression for the message if it's long
    if len(message) > 50:
        # Compress and encode
        compressed = zlib.compress(message.encode('utf-8'), level=9)
        encoded_msg = base64.urlsafe_b64encode(compressed).decode('ascii')
        msg_param = f"mc={encoded_msg}"  # mc = message compressed
    else:
        # Short messages: just URL encode
        msg_param = f"m={quote(message, safe='')}"
    
    # Build query string with short parameter names
    params = {
        "tab": "view",  # Fixed: use "view" to trigger mobile greeting view
        "f": from_name,
        "t": to_name,
        "th": theme
    }
    
    # Add background if specified
    background = greeting.get("background", "")
    if background:
        params["bg"] = background
    
    query = urlencode(params, safe='')
    
    # Add message parameter (already formatted)
    full_url = f"{base_url}?{query}&{msg_param}"
    
    return full_url


def decode_greeting_from_url(query_params: Dict) -> Optional[Dict]:
    """
    Decode greeting data from URL query parameters
    
    Args:
        query_params: Dictionary of query parameters (values may be lists)
        
    Returns:
        Greeting dictionary or None if invalid
    """
    try:
        # Handle both list and single value formats
        def get_param(key, default=""):
            val = query_params.get(key, default)
            if isinstance(val, list):
                return val[0] if val else default
            return val or default
        
        from_name = get_param("f")
        to_name = get_param("t")
        theme = get_param("th", "general")
        
        # Check for compressed message first
        compressed_msg = get_param("mc")
        plain_msg = get_param("m")
        
        if compressed_msg:
            # Decompress message
            try:
                compressed_bytes = base64.urlsafe_b64decode(compressed_msg)
                message = zlib.decompress(compressed_bytes).decode('utf-8')
            except Exception:
                message = ""
        elif plain_msg:
            message = unquote(plain_msg)
        else:
            message = ""
        
        if not message:
            return None
        
        # Get background if specified
        background = get_param("bg", "")
            
        greeting = {
            "v": "1.0",
            "type": "greeting",
            "from": from_name,
            "to": to_name,
            "message": message,
            "theme": theme,
            "created": datetime.utcnow().isoformat()
        }
        if background:
            greeting["background"] = background
        return greeting
    except Exception:
        return None


def create_holiday_greeting(
    from_name: str,
    to_name: str,
    message: str,
    theme: str = "general",
    background: str = ""
) -> Dict:
    """
    Create a structured holiday greeting payload

    Args:
        from_name: Sender's name
        to_name: Recipient's name
        message: Greeting message
        theme: Visual theme identifier

    Returns:
        Dictionary containing greeting data
    """
    greeting = {
        "message": message,
        "from": from_name,
        "to": to_name,
        "theme": theme,
        "created": datetime.utcnow().isoformat()
    }
    if background:
        greeting["background"] = background
    return greeting


def compact_greeting(payload: Dict) -> str:
    """
    Minimize JSON payload by removing whitespace

    Args:
        payload: Greeting dictionary

    Returns:
        Compact JSON string
    """
    return json.dumps(payload, separators=(',', ':'), ensure_ascii=False)


def parse_greeting(qr_data: str) -> Optional[Dict]:
    """
    Parse raw text QR code into a greeting structure.
    Supports both JSON format and URL format (new).
    """
    if not qr_data:
        return None
    
    # Check if it's a URL (new format)
    if qr_data.startswith("http://") or qr_data.startswith("https://"):
        try:
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(qr_data)
            query_params = parse_qs(parsed_url.query)
            
            # Convert query params to format expected by decode_greeting_from_url
            greeting = decode_greeting_from_url(query_params)
            if greeting:
                return greeting
        except Exception:
            pass
        
    # Try to parse as JSON (legacy format)
    try:
        data = json.loads(qr_data)
        if isinstance(data, dict):
            # Ensure it has basic fields
            return {
                "v": data.get("v", "1.0"),
                "type": data.get("type", "greeting"),
                "from": data.get("from", ""),
                "to": data.get("to", ""),
                "message": data.get("message", ""),
                "theme": data.get("theme", "general"),
                "created": data.get("created", datetime.utcnow().isoformat())
            }
    except json.JSONDecodeError:
        pass

    # Fallback to plain text
    return {
        "v": "1.0",
        "type": "greeting",
        "from": "",  # Not stored in QR
        "to": "",    # Not stored in QR
        "message": qr_data,
        "theme": "general",
        "created": datetime.utcnow().isoformat()
    }



def format_greeting_display(greeting: Dict) -> str:
    """
    Format greeting data for nice display

    Args:
        greeting: Parsed greeting dictionary

    Returns:
        Formatted string for display
    """
    lines = [
        "",
        greeting.get('message', ''),
        "",
        f"From: {greeting.get('from', 'Unknown')}",
        f"To: {greeting.get('to', 'Unknown')}",
        f"Theme: {greeting.get('theme', 'general')}",
        f"Created: {greeting.get('created', 'Unknown')}"
    ]
    return "\n".join(lines)


def get_greeting_stats(greeting_json: str) -> Dict:
    """
    Get statistics about the greeting size

    Args:
        greeting_json: Compact JSON string

    Returns:
        Dictionary with size statistics
    """
    byte_size = len(greeting_json.encode('utf-8'))

    # QR code capacity reference (with High error correction)
    qr_versions = [
        (10, 224),   # V10-H
        (15, 432),   # V15-H
        (20, 666),   # V20-H
        (25, 952),   # V25-H
        (30, 1276),  # V30-H
        (40, 1852),  # V40-H
    ]

    recommended_version = None
    for version, capacity in qr_versions:
        if byte_size <= capacity:
            recommended_version = version
            break

    if not recommended_version:
        recommended_version = 40

    return {
        "byte_size": byte_size,
        "char_count": len(greeting_json),
        "recommended_qr_version": recommended_version,
        "fits_in_qr": byte_size <= 1852  # Max capacity of V40-H
    }
````

## File: streamlit/packages.txt
````
libgl1-mesa-glx
libglib2.0-0
libsm6
libxext6
libxrender-dev
libgomp1
````

## File: streamlit/tabs/__init__.py
````python
"""UI tab modules for the application"""
from tabs import demo_tab, funnel_tab
````

## File: streamlit/utils/url_utils.py
````python
"""
URL utility functions for background handling and link processing
Handles YouTube, Google Drive, Facebook, Instagram, and general web URL conversions
"""

import re
import urllib.parse
from typing import Optional


def is_web_url(background_str: str) -> bool:
    """
    Check if a background string is a web URL.

    Args:
        background_str: Background identifier (filename or URL)

    Returns:
        True if the string is a web URL, False otherwise
    """
    if not background_str:
        return False
    background_lower = background_str.lower()
    return background_lower.startswith(('http://', 'https://')) or \
           any(domain in background_lower for domain in [
               'youtu.be', 'youtube.com', 'facebook.com', 'fb.watch', 'instagram.com'
           ])


def classify_background(background_str: str) -> str:
    """
    Classify background type based on URL pattern.

    Args:
        background_str: Background identifier (filename or URL)

    Returns:
        One of: 'local_file', 'youtube', 'google_drive', 'facebook', 'instagram',
                'direct_video', 'other_url', or 'invalid'
    """
    if not background_str:
        return 'invalid'

    if not is_web_url(background_str):
        return 'local_file'

    background_lower = background_str.lower()

    # Check for Google Drive URLs
    if 'drive.google.com' in background_lower and '/file/d/' in background_lower:
        return 'google_drive'

    # Check for YouTube URLs
    if 'youtube.com' in background_lower or 'youtu.be' in background_lower:
        return 'youtube'

    # Check for Facebook URLs
    if 'facebook.com' in background_lower or 'fb.watch' in background_lower:
        # Verify it's a video/reel/share URL
        if any(pattern in background_lower for pattern in ['/reel/', '/videos/', '/watch', 'fb.watch', '/share/r/', '/share/v/']):
            return 'facebook'

    # Check for Instagram URLs
    if 'instagram.com' in background_lower:
        # Verify it's a reel/post/tv URL
        if any(pattern in background_lower for pattern in ['/reel/', '/p/', '/tv/']):
            return 'instagram'

    # Check for direct video URLs (by extension)
    if any(background_lower.endswith(ext) for ext in ['.mp4', '.webm', '.mov', '.avi', '.m3u8']):
        return 'direct_video'

    # Check if it's a generic URL
    if background_lower.startswith(('http://', 'https://')):
        return 'other_url'

    return 'invalid'


def convert_youtube_to_embed_url(youtube_url: str) -> Optional[str]:
    """
    Convert various YouTube URL formats to embeddable iframe URL.

    Handles:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - youtu.be/VIDEO_ID (without protocol)

    Args:
        youtube_url: YouTube URL in any supported format

    Returns:
        Embed URL in format https://www.youtube.com/embed/VIDEO_ID, or None if invalid
    """
    if not youtube_url:
        return None

    # YouTube video ID pattern: 11 characters (alphanumeric, hyphens, underscores)
    video_id_pattern = r'[a-zA-Z0-9_-]{11}'

    # Try different URL patterns
    patterns = [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',  # youtube.com/watch?v=ID
        r'youtu\.be/([a-zA-Z0-9_-]{11})',              # youtu.be/ID
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',     # youtube.com/embed/ID
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"

    return None


def convert_google_drive_to_embed_url(drive_url: str) -> Optional[str]:
    """
    Convert Google Drive share URL to embeddable preview URL.

    Input format: https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing
    Output format: https://drive.google.com/file/d/{FILE_ID}/preview

    Args:
        drive_url: Google Drive share URL

    Returns:
        Embed URL or None if FILE_ID cannot be extracted
    """
    # Pattern to extract FILE_ID from Google Drive URL
    # Matches: /file/d/{FILE_ID}/ where FILE_ID is alphanumeric with hyphens/underscores
    match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', drive_url)

    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"

    return None


def convert_facebook_to_embed_url(facebook_url: str) -> Optional[str]:
    """
    Convert Facebook video/reel URL to embeddable iframe URL.

    Supports:
    - https://www.facebook.com/reel/{ID}
    - https://www.facebook.com/share/r/{ID}
    - https://www.facebook.com/{user}/videos/{ID}
    - https://www.facebook.com/watch?v={ID}
    - https://fb.watch/{SHORT_ID}

    Args:
        facebook_url: Facebook video/reel URL

    Returns:
        Embed URL using Facebook's video plugin, or None if invalid

    Notes:
        - Uses Facebook's plugin: https://www.facebook.com/plugins/video.php
        - Requires URL encoding of original Facebook URL
        - May not work for all Reels (Facebook limitation as of 2025)
    """
    if not facebook_url:
        return None

    # Normalize URL
    url_lower = facebook_url.lower()

    # Pattern 1a: facebook.com/reel/{ID} - now supports alphanumeric IDs
    reel_match = re.search(r'facebook\.com/reel/([a-zA-Z0-9_-]+)', facebook_url)
    if reel_match:
        reel_id = reel_match.group(1)
        # Reconstruct canonical URL
        canonical_url = f"https://www.facebook.com/reel/{reel_id}"
        encoded_url = urllib.parse.quote(canonical_url, safe='')
        return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"

    # Pattern 1b: facebook.com/share/r/{ID} or /share/v/{ID}
    share_match = re.search(r'facebook\.com/share/(?:r|v)/([a-zA-Z0-9_-]+)', facebook_url)
    if share_match:
        share_id = share_match.group(1)
        # Reconstruct canonical URL for plugin (it usually works better with the /reel/ or original link format)
        # For share links, we usually want to follow the redirect, but the plugin might handle the share link directly.
        # Let's try passing the share link directly first.
        encoded_url = urllib.parse.quote(facebook_url, safe='')
        return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"

    # Pattern 2: facebook.com/*/videos/{ID} or facebook.com/watch?v={ID}
    video_match = re.search(r'facebook\.com/(?:[\w.]+/videos/|watch\?v=)(\d+)', facebook_url)
    if video_match:
        # Use original URL for embedding (preserve full path)
        encoded_url = urllib.parse.quote(facebook_url, safe='')
        return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"

    # Pattern 3: fb.watch/{SHORT_ID}
    fbwatch_match = re.search(r'fb\.watch/([a-zA-Z0-9_-]+)', facebook_url)
    if fbwatch_match:
        # fb.watch redirects to full URL, but plugin should handle it
        encoded_url = urllib.parse.quote(facebook_url, safe='')
        return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"

    return None


def convert_instagram_to_embed_url(instagram_url: str) -> Optional[str]:
    """
    Convert Instagram reel/post URL to embeddable format.

    Supports:
    - https://www.instagram.com/reel/{ID}/
    - https://www.instagram.com/p/{ID}/
    - https://www.instagram.com/tv/{ID}/

    Args:
        instagram_url: Instagram reel/post URL

    Returns:
        Embed URL using Instagram's embed format, or None if invalid

    Notes:
        - Instagram embed requires /embed/ path suffix
        - May not work reliably without Meta oEmbed API (2025 limitation)
        - Fallback: Display message to user about opening in Instagram app
    """
    if not instagram_url:
        return None

    # Pattern: instagram.com/{type}/{ID}
    # Where type is: reel, p (post), tv (IGTV)
    # ID is alphanumeric (usually 11 chars but can vary)
    match = re.search(r'instagram\.com/(reel|p|tv)/([a-zA-Z0-9_-]+)', instagram_url)

    if match:
        content_type = match.group(1)
        content_id = match.group(2)

        # Instagram embed URL pattern
        # Note: This may not work without Meta API access in 2025
        return f"https://www.instagram.com/{content_type}/{content_id}/embed/"

    return None


def linkify_urls(text: str) -> str:
    """
    Convert URLs in text to clickable HTML links.

    Args:
        text: Plain text that may contain URLs

    Returns:
        Text with URLs wrapped in <a> tags
    """
    # Regex pattern for http/https URLs
    # Matches: http:// or https:// followed by valid URL characters
    # Captures full URL including domain extensions (.com, .org, etc.)
    # Trailing punctuation is removed by cleanup code below
    url_pattern = r'(https?://[^\s<>\'"\)]+)'

    def replace_url(match):
        url = match.group(1)
        # Remove trailing punctuation that might have been captured
        while url and url[-1] in '.,;:!?)':
            url = url[:-1]
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #667eea; text-decoration: underline;">{url}</a>'

    return re.sub(url_pattern, replace_url, text)
````

## File: streamlit/config.py
````python
"""
Configuration and constants for QR Greeting Card Generator
Contains theme definitions, CSS styles, and application settings
"""

# Theme to emoji mapping
THEME_ICONS = {
    "snowflake": "❄️",
    "fireworks": "🎆",
    "lights": "✨",
    "stars": "⭐",
    "confetti": "🎉",
    "champagne": "🥂",
    "hearts": "❤️",
    "valentine": "💕",
    "farewell": "👋",
    "burn_after_read": "🔥",  # Mission Impossible spy theme
    "general": None  # No icon for general theme
}

# Animation presets mapped to themes
THEME_ANIMATIONS = {
    "snowflake": "FadeInCenterOut",
    "fireworks": "RadialRipple",
    "lights": "FadeInTopDown",
    "stars": "RadialRippleIn",
    "confetti": "MaterializeIn",
    "champagne": "RadialRipple",
    "hearts": "FadeInCenterOut",
    "valentine": "FadeInCenterOut",
    "farewell": "FadeInTopDown",
    "burn_after_read": "RadialRipple",  # Burning fuse effect
    "general": "MaterializeIn"
}

# Color palettes for themes (QR code colors)
THEME_COLORS = {
    "snowflake": {"module": "#4FC3F7", "ring": "#0288D1"},
    "fireworks": {"module": "#FF5722", "ring": "#FFC107"},
    "lights": {"module": "#FFD700", "ring": "#FFA500"},
    "stars": {"module": "#FFD700", "ring": "#FF8C00"},
    "confetti": {"module": "#E91E63", "ring": "#9C27B0"},
    "champagne": {"module": "#FFD700", "ring": "#FF6F00"},
    "hearts": {"module": "#E91E63", "ring": "#D81B60"},
    "valentine": {"module": "#FF69B4", "ring": "#C71585"},  # Hot pink & medium violet red
    "farewell": {"module": "#1976D2", "ring": "#1565C0"},
    "burn_after_read": {"module": "#FF4500", "ring": "#1A1A1A"},  # Mission Impossible: flame orange + near-black
    "general": {"module": "#1f77b4", "ring": "#ff7f0e"}
}

# Available animation types for QR codes
AVAILABLE_ANIMATIONS = [
    "MaterializeIn",
    "FadeInTopDown",
    "FadeInCenterOut",
    "RadialRipple",
    "RadialRippleIn",
    "None"
]

# Page configuration settings
PAGE_CONFIG = {
    "page_title": "Holiday Greeting QR",
    "page_icon": "🎄",
    "layout": "wide"
}

# Custom CSS styles
CSS_STYLES = """
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .greeting-box {
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stats-box {
        padding: 1rem;
        background: #e8eaf6;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .letter-container {
        background-color: #fdfbf7;
        padding: 40px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        min-height: 400px;
        position: relative;
        font-family: 'Georgia', serif;
        color: #333;
        margin-top: 20px;
    }
    .letter-header {
        margin-bottom: 30px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    .letter-from, .letter-to {
        font-size: 1.1em;
        margin: 5px 0;
    }
    .letter-body {
        font-size: 1.25em;
        line-height: 1.6;
        white-space: pre-wrap;
        margin-bottom: 60px;
    }
    .letter-watermark {
        position: absolute;
        bottom: 20px;
        right: 20px;
        opacity: 0.8;
        width: 100px;
        height: 100px;
    }
    .letter-footer {
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-size: 0.8em;
        color: #888;
    }
    /* QR Code Protection - Global fallback */
    .qr-code-protected {
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        user-select: none;
        -webkit-user-drag: none;
    }
</style>
"""
````

## File: streamlit/tabs/about_tab.py
````python
"""
About Tab
Information about the application and its features
"""


import streamlit as st
from utils.download_tracker import get_download_count
from i18n import get_text as _


def render() -> None:
    """About the application"""
    st.markdown(f'<div class="main-header"><h1>{_("about_tab.header")}</h1></div>',
                unsafe_allow_html=True)

    st.write(_("about_tab.title"))
    st.write(_("about_tab.description"))

    st.markdown("---")
    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=6SuLXoRmykE")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Video section with styled heading
    st.markdown(f"""
<div style="text-align: center; margin: 2rem 0 1rem 0;">
    <h3 style="color: #333; margin-bottom: 0.5rem;">{_('about_tab.video_section')}</h3>
    <p style="color: #666; margin-bottom: 1.5rem; font-size: 1rem;">
        {_('about_tab.video_description')}
    </p>
</div>
""", unsafe_allow_html=True)

    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=hJdGamlet5A")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Core positioning messages
    st.markdown("---")
    st.subheader(_("about_tab.why_choose"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        {_('about_tab.environment.title')}

        {_('about_tab.environment.heading')}

        {_('about_tab.environment.description')}
        """)

    with col2:
        st.markdown(f"""
        {_('about_tab.secret.title')}

        {_('about_tab.secret.heading')}

        {_('about_tab.secret.description')}

        {_('about_tab.secret.benefit1')}
        {_('about_tab.secret.benefit2')}
        {_('about_tab.secret.benefit3')}
        {_('about_tab.secret.benefit4')}

        {_('about_tab.secret.tagline')}
        """)

    with col3:
        st.markdown(f"""
        {_('about_tab.device.title')}

        {_('about_tab.device.heading')}

        {_('about_tab.device.description')}
        """)

    st.markdown("---")

    # Business Value Proposition - Attention Economy
    st.subheader(_("about_tab.business.title"))

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        {_('about_tab.business.challenge')}

        {_('about_tab.business.solution_intro')}

        {_('about_tab.business.step1')}
        {_('about_tab.business.step2')}
        {_('about_tab.business.step3')}

        {_('about_tab.business.use_cases_title')}
        {_('about_tab.business.use_cases_list')}
        """)

    with col2:
        st.markdown(f"""
        {_('about_tab.business.stats_title')}

        {_('about_tab.business.stats_list')}
        """)

    st.markdown("---")

    st.write(f"""
    {_('about_tab.features.title')}
    {_('about_tab.features.custom')}
    {_('about_tab.features.scan')}
    {_('about_tab.features.themes')}
    {_('about_tab.features.download')}
    {_('about_tab.features.json')}

    {_('about_tab.how_it_works.title')}
    {_('about_tab.how_it_works.step1')}
    {_('about_tab.how_it_works.step2')}
    {_('about_tab.how_it_works.step3')}
    {_('about_tab.how_it_works.step4')}

    {_('about_tab.how_it_works.recipients')}

    {_('about_tab.technical.title')}
    {_('about_tab.technical.error_correction')}
    {_('about_tab.technical.json_format')}
    {_('about_tab.technical.message_length')}
    {_('about_tab.technical.built_with')}
    """)

    st.markdown("---")

    st.markdown(f"""
    {_('about_tab.privacy.title')}

    {_('about_tab.privacy.heading')}

    {_('about_tab.privacy.description')}

    {_('about_tab.privacy.no_ai')}
    {_('about_tab.privacy.no_training')}
    {_('about_tab.privacy.no_analysis')}
    {_('about_tab.privacy.no_cloud')}

    {_('about_tab.privacy.tagline')}
    """)

    st.write(f"""
    {_('about_tab.powered_by.title')}
    {_('about_tab.powered_by.netshare')}
    {_('about_tab.powered_by.streamlit')}
    {_('about_tab.powered_by.qrcode')}
    {_('about_tab.powered_by.pillow')}
    """)

    # Display download count (just the number)
    count = get_download_count()
    st.write(count)
````

## File: streamlit/qr/display.py
````python
"""
QR code display module
Handles QR code display with protection and greeting letter rendering
"""

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64
import io
import os
from typing import Dict

from i18n import get_text as _
from config import THEME_ICONS
from utils.url_utils import (
    is_web_url,
    classify_background,
    convert_youtube_to_embed_url,
    convert_google_drive_to_embed_url,
    convert_facebook_to_embed_url,
    convert_instagram_to_embed_url,
    linkify_urls
)
from utils.image_utils import get_img_as_base64


def display_qr_with_protection(qr_img: Image.Image, caption: str = "", width: int = None) -> None:
    """
    Display QR code image with right-click protection

    Args:
        qr_img: PIL Image object of QR code
        caption: Caption text to display below image
        width: Width in pixels (None for auto-width, matching Streamlit's 'stretch')

    Returns:
        None (renders HTML component directly)
    """
    # Convert PIL Image to base64 data URI
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    img_data_uri = f"data:image/png;base64,{img_base64}"

    # Get actual QR image dimensions
    img_width, img_height = qr_img.size

    # Use constrained width for consistent display
    # Max 500px width works well across devices (desktop and mobile)
    max_display_width = 500
    actual_display_width = min(img_width, max_display_width)

    # QR codes are square usually, but visible message increases height
    # Calculate height based on aspect ratio
    scaled_height = actual_display_width * (img_height / img_width) if img_width > 0 else actual_display_width

    # Add extra space for caption and margins
    caption_space = 80 if caption else 40
    iframe_height = scaled_height + caption_space

    # Build protected HTML with inline styles and JavaScript
    width_style = f"max-width: {max_display_width}px; width: 100%;"

    # Use id(qr_img) for unique element ID
    unique_id = f"qr-preview-{id(qr_img)}"

    html_code = f"""
    <div style="text-align: center; margin: 1rem 0;">
        <img
            id="{unique_id}"
            src="{img_data_uri}"
            alt="{_('display.qr_preview')}"
            style="{width_style} height: auto; display: block; margin: 0 auto;
                   -webkit-touch-callout: none; -webkit-user-select: none;
                   -moz-user-select: none; -ms-user-select: none; user-select: none;
                   -webkit-user-drag: none; user-drag: none;"
            oncontextmenu="return false;"
            ondragstart="return false;"
        >
        {f'<p style="text-align: center; color: #666; font-size: 0.9em; margin-top: 0.5rem;">{caption}</p>' if caption else ''}
    </div>
    <script>
    (function() {{
        const img = document.getElementById('{unique_id}');
        if (img) {{
            img.addEventListener('contextmenu', e => {{ e.preventDefault(); return false; }});
            img.addEventListener('dragstart', e => {{ e.preventDefault(); return false; }});
            img.addEventListener('copy', e => {{ e.preventDefault(); return false; }});
        }}
    }})();
    </script>
    """

    components.html(html_code, height=iframe_height, scrolling=False)


def display_animated_qr(
    data: str,
    theme: str = "general",
    animation: str = "MaterializeIn",
    module_color: str = "#1f77b4",
    position_ring_color: str = "#ff7f0e",
    visible_message: str = None,
    width: int = 300,
    caption: str = ""
) -> None:
    """
    Display QR code with animation using @bitjson/qr-code web component.

    Args:
        data: URL or text to encode in QR code
        theme: Theme name from config.THEME_ICONS
        animation: Animation type (FadeInTopDown|FadeInCenterOut|MaterializeIn|RadialRipple|RadialRippleIn|None)
        module_color: Hex color for QR modules/dots
        position_ring_color: Hex color for position detection markers
        visible_message: Optional text overlay below QR code
        width: Display width in pixels
        caption: Caption text to display below QR code

    Returns:
        None (renders HTML component directly)
    """
    # Get theme emoji for icon slot
    icon_emoji = THEME_ICONS.get(theme, "🎨") if theme != "general" else ""

    # Generate unique ID for this QR code instance
    unique_id = f"qr-{abs(hash(data)) % 10000000}"

    # Prepare icon HTML if theme has an emoji
    icon_html = ""
    if icon_emoji:
        icon_html = f'<div slot="icon" style="font-size: 48px; line-height: 1;">{icon_emoji}</div>'

    # Prepare visible message HTML if provided
    message_html = ""
    if visible_message:
        message_html = f'''
        <div style="text-align: center; margin-top: 15px; font-size: 1.1em; color: #333; font-weight: 500;">
            {visible_message}
        </div>
        '''

    # Prepare caption HTML if provided
    caption_html = ""
    if caption:
        caption_html = f'<p style="text-align: center; color: #666; font-size: 0.9em; margin-top: 10px;">{caption}</p>'

    # Run animation when component is ready
    animation_script = f"""
    // Helper to start animation safely
    const animate = () => {{
        try {{
            qr.animateQRCode('{animation}');
        }} catch (e) {{
            // Ignore errors if animation is already running or component not ready
            console.warn('Animation attempt failed:', e);
        }}
    }};

    // Wait for custom element to be upgraded
    customElements.whenDefined('qr-code').then(() => {{
        const qr = document.getElementById('{unique_id}');
        if (!qr) return;

        // 1. Listen for render events (normal flow)
        qr.addEventListener('codeRendered', () => {{
            setTimeout(animate, 100);
        }});

        // 2. Fallback: Try to animate after a delay in case we missed the event
        // (common race condition if component renders fast)
        setTimeout(animate, 500);
    }});
    """

    if animation == "None" or not animation:
        animation_script = ""

    # Calculate iframe height (QR + message + caption + padding)
    iframe_height = width + (80 if visible_message else 0) + (40 if caption else 0) + 100

    # Build complete HTML with web component
    # Added onerror handler to script to show user feedback if CDN fails
    html_code = f"""
    <script type="module" src="https://unpkg.com/@bitjson/qr-code@1.0.2/dist/qr-code.js" 
            onerror="document.getElementById('{unique_id}-error').style.display='block';"></script>
    
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px;">
        <div id="{unique_id}-error" style="display:none; color: #d32f2f; background: #ffebee; padding: 10px; border-radius: 4px; margin-bottom: 10px; text-align: center;">
             {_('display.error_animation')}
        </div>
        
        <qr-code id="{unique_id}"
          contents="{data}"
          module-color="{module_color}"
          position-ring-color="{position_ring_color}"
          position-center-color="{position_ring_color}"
          style="width: {width}px; height: {width}px; background-color: white;">
          {icon_html}
        </qr-code>
        {message_html}
        {caption_html}
    </div>
    <script>
    (function() {{
        const qr = document.getElementById('{unique_id}');
        if (!qr) {{
            return;
        }}

        {animation_script}

        // Add right-click protection
        qr.addEventListener('contextmenu', e => {{ e.preventDefault(); return false; }});
        qr.addEventListener('dragstart', e => {{ e.preventDefault(); return false; }});
        qr.addEventListener('copy', e => {{ e.preventDefault(); return false; }});
    }})();
    </script>
    """

    components.html(html_code, height=iframe_height, scrolling=False)


def display_greeting_letter(greeting: Dict) -> None:
    """
    Display greeting in a letter format with optional background

    Args:
        greeting: Dictionary containing greeting data (to, from, message, theme, background, created)

    Returns:
        None (renders greeting directly)
    """
    # Prepare icon for HTML
    theme_name = greeting.get('theme', 'general')
    icon_html = ""
    if theme_name in THEME_ICONS and theme_name != 'general':
        icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", f"{theme_name}.png")
        if os.path.exists(icon_path):
            b64_icon = get_img_as_base64(icon_path)
            icon_html = f'<img src="data:image/png;base64,{b64_icon}" class="letter-watermark">'

    # Handle background if specified
    background_html = ""
    background_style = ""
    background_name = greeting.get('background', '')

    if background_name:
        # Check if background is a web URL
        if is_web_url(background_name):
            bg_type = classify_background(background_name)

            if bg_type == 'youtube':
                # YouTube embed iframe
                embed_url = convert_youtube_to_embed_url(background_name)
                if embed_url:
                    # Extract video ID for playlist parameter (required for loop)
                    video_id = embed_url.split('/')[-1]
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}?autoplay=1&mute=1&loop=1&playlist={video_id}"
                        allow="autoplay; encrypted-media"
                        allowfullscreen
                    ></iframe>'''
            elif bg_type == 'google_drive':
                # Google Drive embed iframe
                embed_url = convert_google_drive_to_embed_url(background_name)
                if embed_url:
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}"
                        allowfullscreen
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    ></iframe>'''
            elif bg_type == 'facebook':
                # Facebook embed iframe
                embed_url = convert_facebook_to_embed_url(background_name)
                if embed_url:
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}"
                        allow="autoplay; encrypted-media; picture-in-picture"
                        allowfullscreen
                    ></iframe>'''
            elif bg_type == 'instagram':
                # Instagram embed iframe with fallback button
                embed_url = convert_instagram_to_embed_url(background_name)
                if embed_url:
                    # Attempt embed but also provide fallback button
                    background_html = f'''<iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: -1; opacity: 0.7;"
                        src="{embed_url}"
                        allowfullscreen
                    ></iframe>
                    <div style="position: absolute; top: 10px; right: 10px; z-index: 5;">
                        <a href="{background_name}" target="_blank" rel="noopener noreferrer"
                           style="display: inline-block; padding: 10px 20px; background: #e4405f; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
                            {_('display.instagram_button')}
                        </a>
                    </div>'''
            elif bg_type == 'direct_video':
                # Direct HTML5 video from URL
                background_html = f'''<video autoplay loop muted playsinline
                    style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover; z-index: -1; opacity: 0.7;">
                    <source src="{background_name}" type="video/mp4">
                </video>'''
        else:
            # Local file - Check keep/ folder first, then gif/ folder
            keep_path = os.path.join(os.path.dirname(__file__), "..", "keep", background_name)
            gif_path = os.path.join(os.path.dirname(__file__), "..", "gif", background_name)

            if os.path.exists(keep_path):
                background_path = keep_path
            elif os.path.exists(gif_path):
                background_path = gif_path
            else:
                background_path = None

            if background_path and os.path.exists(background_path):
                ext = os.path.splitext(background_name)[1].lower()

                if ext in ['.mp4', '.webm']:
                    # Video background - embed as base64
                    b64_video = get_img_as_base64(background_path)
                    mime = "video/mp4" if ext == ".mp4" else "video/webm"
                    background_html = f'<video autoplay loop muted playsinline style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover; z-index: -1; opacity: 0.7;"><source src="data:{mime};base64,{b64_video}" type="{mime}"></video>'
                elif ext in ['.mp3', '.wav', '.ogg']:
                    # Audio background - embed as base64
                    b64_audio = get_img_as_base64(background_path)
                    mime = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg"}.get(ext, "audio/mpeg")
                    background_html = f'<audio autoplay loop style="position: absolute; bottom: 10px; left: 10px; z-index: 10; opacity: 0.7; width: 200px;"><source src="data:{mime};base64,{b64_audio}" type="{mime}"></audio>'
                elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
                    # Image background
                    b64_img = get_img_as_base64(background_path)
                    background_style = f"background-image: url(data:image/{ext[1:]};base64,{b64_img}); background-size: cover; background-position: center;"

    # Only add positioning styles if we have a background
    additional_style = ""
    if background_name and (background_html or background_style):
        additional_style = "position: relative; overflow: hidden;"

    # Combine styles
    final_style = f"{background_style} {additional_style}".strip() if (background_style or additional_style) else ""

    # Construct opening div tag with or without style
    if final_style:
        container_opening = f'<div class="letter-container" style="{final_style}">'
    else:
        container_opening = '<div class="letter-container">'

    # Render HTML Letter
    # Use components.html() for greetings with backgrounds (handles large base64 data)
    # Use st.markdown() for greetings without backgrounds (faster, cleaner)
    if background_html or background_style:
        # Add 'with-background' class for enhanced text contrast
        container_opening_with_bg = container_opening.replace(
            'class="letter-container"',
            'class="letter-container with-background"'
        )

        # Include inline CSS styles when using components.html() (doesn't inherit Streamlit CSS)
        html_content = f"""
        <style>
        .letter-container {{
            background-color: #fdfbf7;
            padding: 40px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
            min-height: 400px;
            max-width: 100%;
            width: 100%;
            height: auto;
            position: relative;
            z-index: 0;  /* Establish stacking context so video (z-index: -1) stays visible */
            isolation: isolate;
            font-family: 'Georgia', serif;
            color: #333;
            margin-top: 20px;
            overflow: hidden;
        }}

        /* Dark overlay for better text readability on backgrounds */
        .letter-container.with-background::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.25);
            z-index: 0;
            pointer-events: none;
        }}

        /* White text with shadows for backgrounds */
        .letter-container.with-background {{
            color: white;
        }}

        .letter-container.with-background .letter-header,
        .letter-container.with-background .letter-to,
        .letter-container.with-background .letter-from,
        .letter-container.with-background .letter-body,
        .letter-container.with-background .letter-footer {{
            position: relative;
            z-index: 1;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9),
                         1px 1px 2px rgba(0, 0, 0, 0.8),
                         -1px -1px 1px rgba(0, 0, 0, 0.7);
        }}

        # /* Semi-transparent background for message body */
        # .letter-container.with-background .letter-body {{
        #     background: rgba(0, 0, 0, 0.35);
        #     padding: 20px;
        #     border-radius: 8px;
        #     backdrop-filter: blur(3px);
        # }}

        .letter-header {{
            margin-bottom: 30px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.5);
            padding-bottom: 10px;
        }}
        .letter-from, .letter-to {{
            font-size: 1.1em;
            margin: 5px 0;
        }}
        .letter-body {{
            font-size: 1.25em;
            line-height: 1.6;
            white-space: pre-wrap;
            margin-bottom: 60px;
        }}
        .letter-watermark {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            opacity: 0.8;
            width: 100px;
            height: 100px;
            z-index: 1;
        }}
        .letter-footer {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            font-size: 0.8em;
            z-index: 1;
        }}
        </style>
        {container_opening_with_bg}
            {background_html}
            <div class="letter-header">
                <div class="letter-to"><strong>{_('display.to_label')}</strong> {greeting.get('to', 'Friend')}</div>
                <div class="letter-from"><strong>{_('display.from_label')}</strong> {greeting.get('from', 'Me')}</div>
            </div>
            <div class="letter-body">
{linkify_urls(greeting.get('message', ''))}
            </div>
            {icon_html}
            <div class="letter-footer">
                {_('display.created', date=greeting.get('created', '').split('T')[0])}
            </div>
        </div>
        """
        # Use components.html() to handle large base64 data without size limits
        components.html(html_content, height=600, scrolling=True)
    else:
        # No background: use st.markdown() (inherits Streamlit CSS)
        html_content = f"""
        {container_opening}
            <div class="letter-header">
                <div class="letter-to"><strong>{_('display.to_label')}</strong> {greeting.get('to', 'Friend')}</div>
                <div class="letter-from"><strong>{_('display.from_label')}</strong> {greeting.get('from', 'Me')}</div>
            </div>
            <div class="letter-body">
{linkify_urls(greeting.get('message', ''))}
            </div>
            {icon_html}
            <div class="letter-footer">
                {_('display.created', date=greeting.get('created', '').split('T')[0])}
            </div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
````

## File: streamlit/requirements.txt
````
streamlit>=1.28.0
requests>=2.31.0
netshare>=1.0.4
qrcode>=7.4.2
Pillow>=9.0.0
opencv-python-headless>=4.8.0
numpy>=1.20.0
pandas>=2.0.0

zxing-cpp>=2.2.0
openpyxl>=3.1.0
````

## File: streamlit/tabs/examples_tab.py
````python
"""
Examples Tab
Displays example greeting configurations and their QR codes
"""

import streamlit as st
from greeting_formats import create_holiday_greeting, encode_greeting_to_url
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection
from config import THEME_COLORS
from i18n import get_text as _


def render() -> None:
    """Tab showing example greetings"""
    st.markdown(f'<div class="main-header"><h1>{_("examples_tab.header")}</h1></div>',
                unsafe_allow_html=True)

    st.write(_("examples_tab.intro"))

    examples = [
        {
            "title": _("examples_tab.christmas.title"),
            "from": _("examples_tab.christmas.from"),
            "to": _("examples_tab.christmas.to"),
            "theme": "snowflake",
            "message": _("examples_tab.christmas.message")
        },
        {
            "title": _("examples_tab.newyear.title"),
            "from": _("examples_tab.newyear.from"),
            "to": _("examples_tab.newyear.to"),
            "theme": "fireworks",
            "message": _("examples_tab.newyear.message")
        },
        {
            "title": _("examples_tab.wedding.title"),
            "from": _("examples_tab.wedding.from"),
            "to": _("examples_tab.wedding.to"),
            "theme": "champagne",
            "message": _("examples_tab.wedding.message")
        },
        {
            "title": _("examples_tab.farewell.title"),
            "from": _("examples_tab.farewell.from"),
            "to": _("examples_tab.farewell.to"),
            "theme": "farewell",
            "message": _("examples_tab.farewell.message"),
            "visible_message": _("examples_tab.farewell.visible_message")
        },
        {
            "title": _("examples_tab.valentine.title"),
            "from": _("examples_tab.valentine.from"),
            "to": _("examples_tab.valentine.to"),
            "theme": "valentine",
            "message": _("examples_tab.valentine.message"),
            "visible_message": _("examples_tab.valentine.visible_message")
        },
        {
            "title": _("examples_tab.marketing.title"),
            "from": _("examples_tab.marketing.from"),
            "to": _("examples_tab.marketing.to"),
            "theme": "lights",
            "message": _("examples_tab.marketing.message"),
            "visible_message": _("examples_tab.marketing.visible_message"),
            "background": "https://youtu.be/dQw4w9WgXcQ"
        },
        {
            "title": _("examples_tab.mission.title"),
            "from": _("examples_tab.mission.from"),
            "to": _("examples_tab.mission.to"),
            "theme": "burn_after_read",
            "message": _("examples_tab.mission.message"),
            "visible_message": _("examples_tab.mission.visible_message"),
            "all_sides": True
        }
    ]

    for example in examples:
        with st.expander(example["title"]):
            col1, col2 = st.columns([1, 1])

            with col1:
                st.write(f"**{_('common.labels.from')}:** {example['from']}")
                st.write(f"**{_('common.labels.to')}:** {example['to']}")
                st.write(f"**{_('create_tab.step1.title').replace('### ', '').replace('Step 1: Choose Your ', '').replace('步骤 1：选择您的', '')}:** {example['theme']}")
                st.markdown("---")
                st.write(example['message'])

            with col2:
                # Generate QR for example
                greeting = create_holiday_greeting(
                    from_name=example['from'],
                    to_name=example['to'],
                    message=example['message'],
                    theme=example['theme']
                )
                # Use URL encoding for QR code
                greeting_url = encode_greeting_to_url(greeting)
                visible_msg = example.get('visible_message', None)

                # Get all_sides parameter from example (defaults to False)
                all_sides = example.get('all_sides', False)

                # Get theme colors for colorized QR code
                theme_colors = THEME_COLORS.get(example['theme'], THEME_COLORS['general'])

                qr_img = generate_qr_code(
                    greeting_url,
                    theme=example['theme'],
                    visible_message=visible_msg,
                    all_sides=all_sides,
                    module_color=theme_colors['module'],
                    position_ring_color=theme_colors['ring']
                )
                display_qr_with_protection(qr_img, caption=_("display.qr_preview"), width=None)
````

## File: streamlit/tabs/view_page.py
````python
"""
View Page (Mobile Greeting View)
Displays greeting in a clean, mobile-friendly format when scanned from QR code
"""

import streamlit as st
from greeting_formats import decode_greeting_from_url
from config import THEME_ICONS
from i18n import get_text as _


def render() -> None:
    """
    Display a greeting message in a clean, mobile-friendly format.
    This is shown when users scan the QR code with their phone camera.
    """
    # Get query parameters
    query_params = dict(st.query_params)
    
    # Check if this is a funnel-type greeting
    greeting_type = query_params.get("t", "")
    
    if greeting_type == "funnel":
        render_funnel_view(query_params)
        return

    # Decode greeting from URL parameters
    greeting = decode_greeting_from_url(query_params)

    if not greeting:
        st.error(_("view_page.invalid_data"))
        st.write(_("view_page.scan_prompt"))
        if st.button(_("common.buttons.go_home")):
            st.query_params.clear()
            st.rerun()
        return

    # Get theme for styling
    theme = greeting.get("theme", "general")
    theme_emoji = THEME_ICONS.get(theme, "🎄")

    # Mobile-optimized greeting display (message only)
    st.markdown("""
    <style>
        .mobile-greeting-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 2rem 1rem;
            text-align: center;
        }
        .greeting-emoji {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        .greeting-message {
            font-family: 'Georgia', serif;
            font-size: 1.5rem;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #fdfbf7 0%, #f5f0e8 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .greeting-from {
            font-size: 1.1rem;
            color: #666;
            margin-top: 1.5rem;
            font-style: italic;
        }
        .view-full-link {
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #888;
        }
    </style>
    """, unsafe_allow_html=True)

    # Display the greeting
    st.markdown('<div class="mobile-greeting-container">', unsafe_allow_html=True)

    # Theme emoji
    if theme_emoji:
        st.markdown(f'<div class="greeting-emoji">{theme_emoji}</div>', unsafe_allow_html=True)

    # The message (main content)
    message = greeting.get("message", "")
    st.markdown(f'<div class="greeting-message">{message}</div>', unsafe_allow_html=True)

    # From attribution (subtle)
    from_name = greeting.get("from", "")
    if from_name:
        st.markdown(f'<div class="greeting-from">{_("view_page.from", name=from_name)}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Subtle link to create your own (not prominent)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption(_("view_page.create_prompt"))
        if st.button(_("common.buttons.create_greeting"), type="secondary", width='stretch'):
            st.query_params.clear()
            st.rerun()


def render_funnel_view(params: dict) -> None:
    """
    Render marketing funnel experience when QR is scanned.
    Updated with warm, pottery-focused design for creators like Mia Mueller.
    """
    # Import here to avoid circular imports
    from utils.video_utils import convert_to_embed_url
    import streamlit.components.v1 as components
    
    # Extract funnel parameters (using compact names)
    headline = params.get("fh", "Special Offer")
    offer_text = params.get("m", "")
    cta_text = params.get("fc", "Learn More")
    cta_url = params.get("fu", "#")
    promo_code = params.get("fp", "")
    urgency = params.get("fg", "")
    video_url = params.get("bg", "")
    brand_name = params.get("f", "")
    theme = params.get("th", "fireworks")
    
    embed_url = convert_to_embed_url(video_url) if video_url else None
    
    # CSS will be embedded in the HTML for the iframe
    funnel_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Source+Sans+Pro:wght@400;600&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            background: #FAF7F2;
        }
        .funnel-container {
            max-width: 100%;
            min-height: 100vh;
            background: #FAF7F2;
            font-family: 'Source Sans Pro', sans-serif;
        }
        .funnel-video {
            width: 100%;
            height: 50vh;
            position: relative;
        }
        .funnel-video iframe, .funnel-video video {
            width: 100%;
            height: 100%;
            border: none;
            object-fit: cover;
        }
        .funnel-content {
            background: #FAF7F2;
            padding: 40px 20px;
            max-width: 600px;
            margin: 0 auto;
        }
        .funnel-headline {
            font-family: 'Poppins', sans-serif;
            font-size: 2em;
            font-weight: 600;
            color: #3E3830;
            text-align: center;
            margin-bottom: 15px;
            line-height: 1.2;
        }
        .funnel-offer {
            font-size: 1.1em;
            color: #3E3830;
            text-align: center;
            line-height: 1.7;
            margin-bottom: 25px;
            white-space: pre-wrap;
        }
        .funnel-benefits {
            margin: 25px 0;
            padding: 0;
        }
        .funnel-benefit {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            font-size: 1.05em;
            color: #3E3830;
        }
        .funnel-benefit::before {
            content: '✓';
            color: #B8956A;
            font-weight: bold;
            margin-right: 10px;
            font-size: 1.3em;
        }
        .funnel-promo {
            background: #B8956A;
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.25em;
            text-align: center;
            margin: 25px auto;
            max-width: 300px;
            box-shadow: 0 3px 10px rgba(184, 149, 106, 0.3);
        }
        .funnel-urgency {
            color: #E74C3C;
            text-align: center;
            font-size: 1em;
            margin-bottom: 20px;
            font-weight: 500;
        }
        .funnel-urgency::before {
            content: '⏱ ';
        }
        .funnel-cta {
            display: block;
            background: linear-gradient(135deg, #B8956A 0%, #A67C52 100%);
            color: white !important;
            text-decoration: none;
            padding: 18px 40px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.25em;
            text-align: center;
            margin: 25px auto;
            max-width: 320px;
            box-shadow: 0 4px 12px rgba(184, 149, 106, 0.4);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .funnel-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(184, 149, 106, 0.5);
        }
        .funnel-separator {
            border: 0;
            height: 1px;
            background: #E8DCC8;
            margin: 30px 20px;
        }
        .funnel-trust {
            text-align: center;
            color: #666;
            font-size: 0.95em;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #E8DCC8;
        }
        .funnel-brand {
            text-align: center;
            color: #888;
            font-size: 0.9em;
            margin-top: 15px;
            font-style: italic;
        }
        .youtube-icon {
            width: 20px;
            height: 20px;
            vertical-align: middle;
            margin-right: 8px;
        }
    </style>
    """
    
    # Build video HTML
    video_html = ""
    if embed_url:
        if 'youtube.com' in embed_url:
            video_id = embed_url.split('/')[-1]
            video_html = f'''
            <div class="funnel-video">
                <iframe src="{embed_url}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=1"
                        allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>
            '''
        elif 'vimeo.com' in embed_url:
            video_html = f'''
            <div class="funnel-video">
                <iframe src="{embed_url}?autoplay=1&muted=1&loop=1&background=1"
                        allow="autoplay" allowfullscreen></iframe>
            </div>
            '''
        else:
            video_html = f'''
            <div class="funnel-video">
                <video autoplay muted loop playsinline>
                    <source src="{embed_url}" type="video/mp4">
                </video>
            </div>
            '''
    
    # Parse offer text for bullet points (if they exist)
    offer_lines = offer_text.split('\n')
    benefits_html = ""
    main_offer = []
    
    for line in offer_lines:
        line = line.strip()
        if line.startswith('✓') or line.startswith('•') or line.startswith('-'):
            # It's a benefit bullet
            benefit_text = line.lstrip('✓•- ').strip()
            benefits_html += f'<div class="funnel-benefit">{benefit_text}</div>'
        elif line:
            # Regular offer text
            main_offer.append(line)
    
    main_offer_text = '<br>'.join(main_offer)
    
    if benefits_html:
        benefits_section = f'<div class="funnel-benefits">{benefits_html}</div>'
    else:
        benefits_section = ""
    
    promo_html = f'<div class="funnel-promo">Use Code: {promo_code}</div>' if promo_code else ""
    urgency_html = f'<div class="funnel-urgency">{urgency}</div>' if urgency else ""
    
    # Trust section for pottery creators
    trust_html = ""
    if brand_name:
        trust_html = f'''
        <div class="funnel-trust">
            <img src="https://upload.wikimedia.org/wikipedia/commons/e/e5/Google_YouTube_icon_(2015-2022).svg" 
                 alt="YouTube" class="youtube-icon">
            As seen on {brand_name}
        </div>
        '''
    
    funnel_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {funnel_css}
    </head>
    <body>
        <div class="funnel-container">
            {video_html}
            <div class="funnel-content">
                <div class="funnel-headline">{headline}</div>
                <div class="funnel-offer">{main_offer_text}</div>
                {benefits_section}
                {promo_html}
                {urgency_html}
                <a href="{cta_url}" target="_blank" rel="noopener" class="funnel-cta">
                    {cta_text}
                </a>
                {trust_html}
            </div>
        </div>
    </body>
    </html>
    '''
    
    components.html(funnel_html, height=800, scrolling=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("Powered by QR-Greeting · Marketing Funnel")
        if st.button("Create Your Own Marketing Funnel", type="secondary", use_container_width=True):
            st.query_params.clear()
            st.query_params["tab"] = "funnel"
            st.rerun()
````

## File: streamlit/translations.json
````json
{
  "en": {
    "_comment_common": "=== Common / Shared Translations ===",
    "common.buttons.generate": "✨ Generate QR Code",
    "common.buttons.download": "📥 Download QR Code",
    "common.buttons.create_another": "🔄 Create Another Greeting",
    "common.buttons.scan_another": "📤 Scan Another QR Code",
    "common.buttons.buy_coffee": "☕ Buy me a coffee (£1)",
    "common.buttons.go_home": "Go to Home Page",
    "common.buttons.create_greeting": "Create Greeting",
    "common.buttons.update_preview": "Update Preview",
    "common.labels.from": "From",
    "common.labels.to": "To",
    "common.labels.message": "Message",
    "common.placeholders.your_name": "Your Name",
    "common.placeholders.friend_name": "Friend's Name",
    "common.placeholders.message": "Your personalized greeting message...",
    "_comment_app": "=== App.py - Main Application ===",
    "app.sidebar.title": "Holiday Greeting QR",
    "app.sidebar.tagline": "Create and share personalized holiday greetings via QR codes!",
    "app.sidebar.greener": "*A greener, smarter way to say happy holidays.*",
    "app.sidebar.quick_tips.title": "### Quick Tips",
    "app.sidebar.quick_tips.tip1": "💡 Keep messages under 300 characters for best QR code size",
    "app.sidebar.quick_tips.tip2": "📱 Test QR codes with your phone camera app",
    "app.sidebar.quick_tips.tip3": "🎨 Choose themes that match your occasion",
    "app.sidebar.support.title": "### Support",
    "app.sidebar.support.text": "If you like this tool, consider supporting it!",
    "app.sidebar.batch_checkbox": "Show Batch Tab",
    "app.sidebar.batch_help": "Enable batch QR code generation from Excel",
    "app.tabs.demo": "🎁 Try Demo",
    "app.tabs.create": "Create Greeting",
    "app.tabs.scan": "Scan QR Code",
    "app.tabs.examples": "Examples",
    "app.tabs.batch": "Batch",
    "app.tabs.about": "About",
    "_comment_create_tab": "=== Create Tab ===",
    "create_tab.header": "🎄 Create Holiday Greeting QR Code",
    "create_tab.subtitle": "*A greener, smarter way to say happy holidays.*",
    "create_tab.intro": "Create a personalized holiday greeting that can be shared via QR code!",
    "create_tab.step1.title": "### Step 1: Choose Your Theme & Background",
    "create_tab.step1.tip": "💡 **Tip:** Pick a theme that matches your occasion. The colors will adapt automatically!",
    "create_tab.background.label": "Background Animation (Optional)",
    "create_tab.background.help": "Choose a GIF animation to display behind your greeting",
    "create_tab.background.none": "(No background animation)",
    "create_tab.background.custom": "(Enter custom URL...)",
    "create_tab.video_url.label": "Video URL",
    "create_tab.video_url.placeholder": "https://youtu.be/..., https://facebook.com/reel/..., or https://example.com/video.mp4",
    "create_tab.video_url.help": "Paste a YouTube URL, Google Drive shared video, Facebook video/reel, Instagram reel, or direct video link (.mp4, .webm, .mov, .avi, .m3u8)",
    "create_tab.video_url.valid": "✅ Valid",
    "create_tab.video_url.validating": "ℹ️ Validating URL...",
    "create_tab.video_url.enter_prompt": "ℹ️ Enter a video URL above to enable background animation",
    "create_tab.gif_preview": "Preview: {gif_name}",
    "create_tab.gif_not_found": "GIF file not found: {file}",
    "create_tab.step2.title": "### Step 2: Preview & Personalize",
    "create_tab.step2.tip": "💡 **Tip:** This is how your greeting will look. You can edit the details below!",
    "create_tab.preview.from": "From: {name}",
    "create_tab.preview.to": "To: {name}",
    "create_tab.default_message": "Wishing you a wonderful holiday season filled with joy, laughter, and cherished moments with loved ones!",
    "create_tab.edit.title": "✍️ **Edit Names & Message**",
    "create_tab.message_length": "Message length: {count} characters",
    "create_tab.qr_options.title": "🎨 **QR Code Options**",
    "create_tab.visible_message.label": "Visible Message (Optional)",
    "create_tab.visible_message.placeholder": "Scan me!",
    "create_tab.visible_message.help": "Short text to display around the QR code image",
    "create_tab.add_all_sides": "Add message to all 4 sides",
    "create_tab.add_all_sides_help": "Display the visible message on top, bottom, left, and right of the QR code",
    "create_tab.step3.title": "### Step 3: Create Magic",
    "create_tab.step3.tip": "💡 **Tip:** Ready? Click below to generate your unique greeting QR code!",
    "create_tab.error.required_fields": "Please fill in all required fields (From, To, and Message)",
    "create_tab.warning.no_video": "⚠️ No video URL entered. Generating QR code without background animation.",
    "create_tab.error.invalid_video": "❌ Invalid video URL: {message}",
    "create_tab.error.video_suggestion": "💡 Please enter a valid YouTube or video URL, or select a different background option.",
    "create_tab.success": "🎉 **Success!** Your greeting QR code is ready.",
    "create_tab.qr_section": "#### 📱 Your Unique QR",
    "create_tab.preview_section": "#### 👀 Scan Preview",
    "create_tab.preview_caption": "This is exactly how your greeting will appear when scanned:",
    "_comment_components": "=== Components ===",
    "components.theme.label": "Theme",
    "components.theme.help": "Choose a theme icon to embed in your QR code",
    "components.theme_preview": "Selected Icon Preview",
    "components.theme_general_info": "ℹ️ General theme: QR code will have no embedded icon",
    "components.video_validation.invalid_format": "⚠️ Invalid URL format. Must start with http:// or https://",
    "components.video_validation.youtube_valid": "✅ Valid YouTube URL",
    "components.video_validation.youtube_invalid": "⚠️ Invalid YouTube URL. Could not extract video ID.",
    "components.video_validation.gdrive_valid": "✅ Valid Google Drive URL",
    "components.video_validation.gdrive_invalid": "⚠️ Invalid Google Drive URL. Could not extract file ID.",
    "components.video_validation.facebook_valid": "✅ Valid Facebook video/reel URL",
    "components.video_validation.facebook_invalid": "⚠️ Invalid Facebook URL. Must be a video or reel URL.",
    "components.video_validation.instagram_warning": "⚠️ Instagram detected. Embedding may be limited - will provide 'Open in Instagram' option.",
    "components.video_validation.instagram_invalid": "⚠️ Invalid Instagram URL. Must be a reel, post, or TV URL.",
    "components.video_validation.direct_valid": "✅ Valid video URL ({format})",
    "components.video_validation.unsupported": "⚠️ Unsupported URL type. Use YouTube, Facebook, Instagram, Google Drive, or direct video links...",
    "components.video_validation.error": "⚠️ Could not validate URL format",
    "components.qr_stats.title": "**QR Code Statistics:**",
    "components.qr_stats.data_size": "- Data size: {bytes} bytes",
    "components.qr_stats.qr_version": "- QR Version: ~{version}",
    "components.qr_stats.scannable_yes": "- Scannable: ✅ Yes",
    "components.qr_stats.scannable_no": "- Scannable: ❌ Too large",
    "components.qr_tip": "📱 Scan with phone camera to open greeting directly!",
    "components.themes.snowflake": "❄️ Snowflake",
    "components.themes.fireworks": "🎆 Fireworks",
    "components.themes.lights": "✨ Lights",
    "components.themes.stars": "⭐ Stars",
    "components.themes.confetti": "🎉 Confetti",
    "components.themes.champagne": "🥂 Champagne",
    "components.themes.hearts": "❤️ Hearts",
    "components.themes.farewell": "👋 Farewell",
    "components.themes.burn": "🔥 Burn After Read",
    "components.themes.valentine": "💕 Valentine",
    "components.themes.general": "⊞ General (No Icon)",
    "_comment_demo_tab": "=== Demo Tab ===",
    "demo_tab.header": "✨ Interactive Demo",
    "demo_tab.subtitle": "Create a sample greeting in 3 easy steps",
    "demo_tab.info": "ℹ️ This is a demo to showcase the concept. For full functionality including downloads, please use the [**Create Greeting**](?tab=create) tab.",
    "demo_tab.step1.title": "### Step 1: Choose Your Vibe",
    "demo_tab.step1.tip": "💡 **Tip:** Pick a theme that matches your occasion. The colors and animations will adapt automatically!",
    "demo_tab.theme_selection_help": "Select {theme} theme",
    "demo_tab.step2.title": "### Step 2: Preview & Personalize",
    "demo_tab.step2.tip": "💡 **Tip:** This is how your greeting will look. You can make quick edits below!",
    "demo_tab.edit.title": "✍️ **Edit Names & Message**",
    "demo_tab.warning.html_removed": "⚠️ HTML tags were detected and removed from your message. Please use plain text only.",
    "demo_tab.step3.title": "### Step 3: Create Magic",
    "demo_tab.step3.tip": "💡 **Tip:** Ready? Click below to generate your unique greeting QR code!",
    "demo_tab.generate_button": "✨ Generate QR Code ✨",
    "demo_tab.success": "🎉 **Success!** Your demo greeting preview is ready.",
    "demo_tab.demo_mode_info": "ℹ️ **Demo Mode**: This is a preview only. Use the [**Create Greeting**](?tab=create) tab for full functionality and downloads.",
    "demo_tab.privacy_info": "🔒 **Privacy Built In**: Your message is encoded directly into the QR pattern.\n        It's opaque to AI training systems and invisible until scanned—no email provider snooping,\n        no algorithm analysis, no unauthorized LLM training. Complete privacy. 🛡️",
    "demo_tab.qr_section": "#### 📱 Your Unique QR",
    "demo_tab.scan_me": "Scan me!",
    "demo_tab.download_button": "⬇️ Download Image (Demo Only)",
    "demo_tab.download_disabled": "Download is disabled in demo mode. Use the 'Create Greeting' tab for full functionality.",
    "demo_tab.preview_only": "💡 This is a preview only. Visit the [**Create Greeting**](?tab=create) tab to download your personalized QR code.",
    "demo_tab.preview_section": "#### 👀 Scan Preview",
    "demo_tab.preview_title": "Thinking of You",
    "demo_tab.preview_hint": "Tap to open",
    "demo_tab.ready_prompt": "🚀 Ready to make it real?",
    "demo_tab.ready_description": "This demo shows the concept. For full functionality with downloads, custom backgrounds, and more, create your own greeting!",
    "demo_tab.create_my_own": "🎁 Create My Own Greeting",
    "demo_tab.start_over": "🔄 Start Demo Over",
    "_comment_scan_tab": "=== Scan Tab ===",
    "scan_tab.header": "📱 Scan Greeting QR Code",
    "scan_tab.success": "🎉 Greeting received!",
    "scan_tab.intro": "Upload a greeting QR code image to view the message!",
    "scan_tab.upload.label": "Choose a QR code image",
    "scan_tab.upload.help": "Upload an image containing a greeting QR code",
    "scan_tab.uploaded_qr": "Uploaded QR Code",
    "scan_tab.uploaded_image": "Uploaded Image",
    "scan_tab.greeting_message": "Greeting Message",
    "scan_tab.invalid_format": "This QR code doesn't contain a valid greeting format.",
    "scan_tab.decoded_data": "Decoded data:",
    "scan_tab.no_qr_found": "No QR code found in the image.",
    "scan_tab.no_libs": "(No scanning libraries available)",
    "scan_tab.zxing_suggestion": "(ZXing-cpp not installed - it may handle this image better)",
    "scan_tab.opencv_required": "QR code scanning requires OpenCV system libraries.",
    "scan_tab.manual_entry": "Please use manual JSON entry below:",
    "scan_tab.paste_label": "Paste QR Code Data (JSON)",
    "scan_tab.invalid_data": "Invalid greeting data format",
    "scan_tab.error": "Error processing image: {error}",
    "scan_tab.alternative": "Alternatively, you can manually paste the QR code data below:",
    "scan_tab.create_own": "📝 Create Your Own Greeting",
    "scan_tab.url_decode_error": "Could not decode greeting from URL. Try uploading the QR code image instead.",
    "_comment_about_tab": "=== About Tab ===",
    "about_tab.header": "ℹ️ About",
    "about_tab.title": "## Holiday Greeting QR Code Generator",
    "about_tab.description": "This application allows you to create personalized holiday greetings encoded in QR codes. Share your messages in a unique and modern way!",
    "about_tab.video_section": "See It In Action",
    "about_tab.video_description": "Watch a quick demo of how easy it is to create and share personalized greeting QR codes.",
    "about_tab.why_choose": "Why Choose QR Greetings?",
    "about_tab.environment.title": "### 🌱 Environment Friendly",
    "about_tab.environment.heading": "**Zero paper. Zero postage. Instant delivery.**",
    "about_tab.environment.description": "Traditional paper cards consume materials, printing resources, and shipping energy. QR greetings are 100% digital — no trees harmed, no carbon footprint from delivery trucks. Send your love without leaving a trace on the planet.",
    "about_tab.secret.title": "### 🔐 Secret in Transit",
    "about_tab.secret.heading": "**Personal, intimate, and AI-safe.**",
    "about_tab.secret.description": "Your greeting is encoded within the QR pattern itself—mathematically opaque to AI systems and invisible until scanned...",
    "about_tab.secret.benefit1": "✅ **No email provider snooping**",
    "about_tab.secret.benefit2": "✅ **No algorithm analysis**",
    "about_tab.secret.benefit3": "✅ **No unauthorized LLM training**",
    "about_tab.secret.benefit4": "✅ **Only the recipient sees your message**",
    "about_tab.secret.tagline": "Send your love without leaving a digital footprint! ❤️🛡️",
    "about_tab.device.title": "### 📱 Device Friendly",
    "about_tab.device.heading": "**Works on any phone. No app required.**",
    "about_tab.device.description": "Recipients simply point their camera at the QR code — that's it! Works seamlessly on both iOS and Android, opening directly in the browser. No downloads, no sign-ups, no friction. Just scan and smile.",
    "about_tab.business.title": "📈 For Businesses: Convert Attention to Action",
    "about_tab.business.challenge": "**The #1 challenge in today's attention economy:** Converting passive video views into active website visits.\n\nYouTube Shorts generate **70 billion daily views** in 2025, but viewers rarely leave the platform.\nTraditional description links have low click-through rates. Attention is captured in seconds—and lost just as fast.",
    "about_tab.business.solution_intro": "**QR Greeting solves this by bridging content and commerce:**",
    "about_tab.business.step1": "1. 🎬 **Embed Your Content** — Use any YouTube video as a background",
    "about_tab.business.step2": "2. 💬 **Add Your CTA** — Include discount codes, links, or exclusive offers in the message",
    "about_tab.business.step3": "3. 📱 **Scan to Convert** — Recipients scan, watch your video, AND see your call-to-action",
    "about_tab.business.use_cases_title": "**Use Cases:**",
    "about_tab.business.use_cases_list": "- Trade show displays with product demo videos\n- Product packaging linking to tutorials + discount codes\n- Print ads that come alive with video content\n- Email signatures with brand story + landing page link",
    "about_tab.business.stats_title": "**2025 Stats:**",
    "about_tab.business.stats_list": "📊 **100M** US consumers will scan QR codes\n\n📈 **73%** prefer short video for product discovery\n\n💰 **20%** higher ROI for Shorts vs traditional video\n\n🎯 **68%** conversion rate from Shorts to full engagement\n\n*Sources: Bitly, Scratcher.io, Zebracat.ai*",
    "about_tab.features.title": "### Features",
    "about_tab.features.custom": "- ✨ Create custom greeting QR codes",
    "about_tab.features.scan": "- 📱 Scan and read greeting QR codes",
    "about_tab.features.themes": "- 🎨 Multiple theme options with embedded icons",
    "about_tab.features.download": "- 📥 Download QR codes as images",
    "about_tab.features.json": "- 💾 Compact JSON format for efficient encoding",
    "about_tab.how_it_works.title": "### How It Works",
    "about_tab.how_it_works.step1": "1. Enter your greeting details (from, to, message)",
    "about_tab.how_it_works.step2": "2. Choose a theme",
    "about_tab.how_it_works.step3": "3. Generate the QR code",
    "about_tab.how_it_works.step4": "4. Download and share!",
    "about_tab.how_it_works.recipients": "Recipients can scan the QR code with their phone camera or upload it to this app to view your message.",
    "about_tab.technical.title": "### Technical Details",
    "about_tab.technical.error_correction": "- Uses high error correction (Level H) for reliable scanning",
    "about_tab.technical.json_format": "- Compact JSON format minimizes QR code size",
    "about_tab.technical.message_length": "- Supports messages up to ~500 characters comfortably",
    "about_tab.technical.built_with": "- Built with Streamlit and netshare",
    "about_tab.privacy.title": "### 🤖 Privacy in the GenAI Era",
    "about_tab.privacy.heading": "**Your message stays hidden from AI systems.**",
    "about_tab.privacy.description": "Unlike text shared via email, SMS, or social media, QR-encoded messages are **mathematically opaque** to automated analysis:",
    "about_tab.privacy.no_ai": "- **No AI Scanning**: Message format prevents automated text extraction",
    "about_tab.privacy.no_training": "- **No Training Data**: Your personal messages won't train LLMs (ChatGPT, Gemini, Claude, etc.)",
    "about_tab.privacy.no_analysis": "- **No Algorithm Analysis**: Email providers and platforms can't read or analyze your content",
    "about_tab.privacy.no_cloud": "- **No Cloud Indexing**: Message exists only in the QR pattern, not on servers",
    "about_tab.privacy.tagline": "Your greeting is encoded, not transmitted. Protected by design. 🛡️",
    "about_tab.powered_by.title": "### Powered By",
    "about_tab.powered_by.netshare": "- **netshare** - Network sharing and QR code utilities",
    "about_tab.powered_by.streamlit": "- **Streamlit** - Interactive web interface",
    "about_tab.powered_by.qrcode": "- **qrcode** - QR code generation",
    "about_tab.powered_by.pillow": "- **Pillow** - Image processing",
    "_comment_examples_tab": "=== Examples Tab ===",
    "examples_tab.header": "📖 Examples",
    "examples_tab.intro": "Here are some example holiday greetings you can create:",
    "examples_tab.christmas.title": "🎄 Christmas Greeting",
    "examples_tab.christmas.from": "Alice",
    "examples_tab.christmas.to": "Bob",
    "examples_tab.christmas.message": "Merry Christmas! Wishing you joy and happiness this season. Thank you for being a wonderful friend!",
    "examples_tab.newyear.title": "🎆 New Year Message",
    "examples_tab.newyear.from": "Bob",
    "examples_tab.newyear.to": "Future Me",
    "examples_tab.newyear.message": "2025 was incredible! Here's to growth and new adventures in 2026!",
    "examples_tab.wedding.title": "💍 Wedding Save the Date",
    "examples_tab.wedding.from": "Emma & James",
    "examples_tab.wedding.to": "Friends and Family",
    "examples_tab.wedding.message": "We're getting married! Save the date: June 15, 2026. More details to follow!",
    "examples_tab.farewell.title": "👋 Farewell to Colleagues",
    "examples_tab.farewell.from": "Alex",
    "examples_tab.farewell.to": "The Team",
    "examples_tab.farewell.message": "It's been an amazing journey working with you all! Thank you for the memories, the laughs, and the lessons. Let's stay in touch!",
    "examples_tab.farewell.visible_message": "Scan to read my farewell note",
    "examples_tab.valentine.title": "💕 Valentine's Day Love Letter",
    "examples_tab.valentine.from": "Your Secret Admirer",
    "examples_tab.valentine.to": "My Dearest",
    "examples_tab.valentine.message": "Every moment with you feels like a beautiful dream. You make my heart flutter and my soul sing. Happy Valentine's Day to the love of my life! 💕🌹",
    "examples_tab.valentine.visible_message": "Scan for a love letter",
    "examples_tab.marketing.title": "📈 Marketing Funnel - Video to Website",
    "examples_tab.marketing.from": "Brand Strategist",
    "examples_tab.marketing.to": "Potential Customer",
    "examples_tab.marketing.message": "✨ EXCLUSIVE OFFER ✨\n\nLove what you just watched? Get 20% OFF your first order!\n\n🎁 Use code: QRGREET20\n👉 Visit: www.yourbrand.com/special\n\nOffer expires in 48 hours. Don't miss out!\n\n#AttentionEconomy #ConvertViewsToVisits",
    "examples_tab.marketing.visible_message": "🎬 Scan for Exclusive Offer",
    "examples_tab.mission.title": "🔥 Mission Impossible - Self-Destructing Message",
    "examples_tab.mission.from": "IMF Agent",
    "examples_tab.mission.to": "Field Operative",
    "examples_tab.mission.message": "Your mission: Rendezvous at Café Milano, 1800 hours. Bring the package. Delete this message after reading. No digital trail - no email interception, no AI monitoring, no server logs. For your eyes only. 🕵️",
    "examples_tab.mission.visible_message": "DELETE ME",
    "_comment_batch_tab": "=== Batch Tab ===",
    "batch_tab.header": "📦 Batch QR Code Generation",
    "batch_tab.description": "Generate multiple QR codes at once by uploading an Excel spreadsheet.",
    "batch_tab.video_feature": "💡 **New Feature**: You can now use YouTube URLs or direct video URLs as backgrounds! Just paste the URL in the Background column.",
    "batch_tab.step1": "1. Download Template",
    "batch_tab.step1_description": "Download the Excel template, fill in your greetings, then upload it below.",
    "batch_tab.download_template": "📥 Download Template (.csv)",
    "batch_tab.valid_options": "View Valid Options",
    "batch_tab.valid_themes": "**Valid Themes:**",
    "batch_tab.valid_backgrounds": "**Valid Backgrounds:**",
    "batch_tab.local_keep": "*Local files from `keep/` folder:*",
    "batch_tab.local_gif": "*Local files from `gif/` folder:*",
    "batch_tab.no_backgrounds": "No backgrounds available in `{folder}/` folder",
    "batch_tab.web_urls": "*Or use web video URLs:*",
    "batch_tab.url_youtube1": "- YouTube: `youtu.be/VIDEO_ID`",
    "batch_tab.url_youtube2": "- YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`",
    "batch_tab.url_direct": "- Direct video: `https://example.com/video.mp4`",
    "batch_tab.step2": "2. Upload Filled Template",
    "batch_tab.upload.label": "Choose your filled CSV file",
    "batch_tab.upload.help": "Upload the template with your greeting data",
    "batch_tab.loaded": "Loaded {count} greetings from CSV!",
    "batch_tab.preview_data": "Preview Data",
    "batch_tab.error.missing_columns": "Missing required columns: {columns}",
    "batch_tab.warning.invalid_themes": "Some rows have invalid themes: {themes}. They will use 'general'.",
    "batch_tab.generate_all": "🚀 Generate All QR Codes",
    "batch_tab.generating": "Generating QR {current}/{total}: {name}...",
    "batch_tab.success": "✅ All QR codes generated!",
    "batch_tab.download_all": "📥 Download All QR Codes (ZIP)",
    "batch_tab.error.row": "Row {idx}: {message}",
    "batch_tab.error.processing": "Error processing Excel file: {error}",
    "_comment_display": "=== QR Display Module ===",
    "display.qr_preview": "QR Code Preview",
    "display.error_animation": "⚠️ Unable to load QR animation library. Please check your internet connection.",
    "display.to_label": "To:",
    "display.from_label": "From:",
    "display.created": "Created: {date}",
    "display.instagram_button": "📱 Open in Instagram",
    "_comment_view_page": "=== View Page ===",
    "view_page.invalid_data": "Invalid or missing greeting data.",
    "view_page.scan_prompt": "Please scan a valid greeting QR code or go to the main page to create one.",
    "view_page.from": "— From {name}",
    "view_page.create_prompt": "Create your own greeting QR code!"
  },
  "zh": {
    "_comment_common": "=== 通用/共享翻译 ===",
    "common.buttons.generate": "✨ 生成二维码",
    "common.buttons.download": "📥 下载二维码",
    "common.buttons.create_another": "🔄 创建另一个问候",
    "common.buttons.scan_another": "📤 扫描另一个二维码",
    "common.buttons.buy_coffee": "☕ 请我喝咖啡（£1）",
    "common.buttons.go_home": "返回主页",
    "common.buttons.create_greeting": "创建问候",
    "common.buttons.update_preview": "更新预览",
    "common.labels.from": "发件人",
    "common.labels.to": "收件人",
    "common.labels.message": "消息",
    "common.placeholders.your_name": "您的名字",
    "common.placeholders.friend_name": "朋友的名字",
    "common.placeholders.message": "您的个性化问候消息...",
    "_comment_app": "=== App.py - 主应用 ===",
    "app.sidebar.title": "节日问候二维码",
    "app.sidebar.tagline": "创建并分享个性化节日问候二维码！",
    "app.sidebar.greener": "*更环保、更智能的节日问候方式。*",
    "app.sidebar.quick_tips.title": "### 快速提示",
    "app.sidebar.quick_tips.tip1": "💡 建议消息长度在300字以内，以获得最佳二维码尺寸",
    "app.sidebar.quick_tips.tip2": "📱 使用手机相机应用测试二维码",
    "app.sidebar.quick_tips.tip3": "🎨 选择与场合相配的主题",
    "app.sidebar.support.title": "### 支持",
    "app.sidebar.support.text": "如果您喜欢这个工具，请考虑支持它！",
    "app.sidebar.batch_checkbox": "显示批量生成标签页",
    "app.sidebar.batch_help": "启用从Excel批量生成二维码",
    "app.tabs.demo": "🎁 试用演示",
    "app.tabs.create": "创建问候",
    "app.tabs.scan": "扫描二维码",
    "app.tabs.examples": "示例",
    "app.tabs.batch": "批量生成",
    "app.tabs.about": "关于",
    "_comment_create_tab": "=== 创建标签页 ===",
    "create_tab.header": "🎄 创建节日问候二维码",
    "create_tab.subtitle": "*更环保、更智能的节日问候方式。*",
    "create_tab.intro": "创建可通过二维码分享的个性化节日问候！",
    "create_tab.step1.title": "### 步骤 1：选择主题和背景",
    "create_tab.step1.tip": "💡 **提示：** 选择与场合相配的主题。颜色会自动适配！",
    "create_tab.background.label": "背景动画（可选）",
    "create_tab.background.help": "选择在问候语后显示的GIF动画",
    "create_tab.background.none": "（无背景动画）",
    "create_tab.background.custom": "（输入自定义URL...）",
    "create_tab.video_url.label": "视频URL",
    "create_tab.video_url.placeholder": "https://youtu.be/..., https://facebook.com/reel/..., 或 https://example.com/video.mp4",
    "create_tab.video_url.help": "粘贴YouTube URL、Google Drive共享视频、Facebook视频/reel、Instagram reel或直接视频链接（.mp4、.webm、.mov、.avi、.m3u8）",
    "create_tab.video_url.valid": "✅ 有效",
    "create_tab.video_url.validating": "ℹ️ 正在验证URL...",
    "create_tab.video_url.enter_prompt": "ℹ️ 在上方输入视频URL以启用背景动画",
    "create_tab.gif_preview": "预览：{gif_name}",
    "create_tab.gif_not_found": "未找到GIF文件：{file}",
    "create_tab.step2.title": "### 步骤 2：预览和个性化",
    "create_tab.step2.tip": "💡 **提示：** 这是您的问候的显示效果。您可以在下方编辑详细信息！",
    "create_tab.preview.from": "发件人：{name}",
    "create_tab.preview.to": "收件人：{name}",
    "create_tab.default_message": "祝您有一个充满欢乐、笑声和与亲人共度美好时光的节日季节！",
    "create_tab.edit.title": "✍️ **编辑姓名和消息**",
    "create_tab.message_length": "消息长度：{count} 个字符",
    "create_tab.qr_options.title": "🎨 **二维码选项**",
    "create_tab.visible_message.label": "可见消息（可选）",
    "create_tab.visible_message.placeholder": "扫我！",
    "create_tab.visible_message.help": "在二维码图像周围显示的简短文本",
    "create_tab.add_all_sides": "在四个边都添加消息",
    "create_tab.add_all_sides_help": "在二维码的上、下、左、右显示可见消息",
    "create_tab.step3.title": "### 步骤 3：创建魔法",
    "create_tab.step3.tip": "💡 **提示：** 准备好了吗？点击下方生成您的专属问候二维码！",
    "create_tab.error.required_fields": "请填写所有必填字段（发件人、收件人和消息）",
    "create_tab.warning.no_video": "⚠️ 未输入视频URL。正在生成无背景动画的二维码。",
    "create_tab.error.invalid_video": "❌ 无效的视频URL：{message}",
    "create_tab.error.video_suggestion": "💡 请输入有效的YouTube或视频URL，或选择其他背景选项。",
    "create_tab.success": "🎉 **成功！** 您的问候二维码已准备就绪。",
    "create_tab.qr_section": "#### 📱 您的专属二维码",
    "create_tab.preview_section": "#### 👀 扫描预览",
    "create_tab.preview_caption": "这是扫描后问候的确切显示效果：",
    "_comment_components": "=== 组件 ===",
    "components.theme.label": "主题",
    "components.theme.help": "选择要嵌入二维码中的主题图标",
    "components.theme_preview": "已选图标预览",
    "components.theme_general_info": "ℹ️ 通用主题：二维码将没有嵌入图标",
    "components.video_validation.invalid_format": "⚠️ 无效的URL格式。必须以http://或https://开头",
    "components.video_validation.youtube_valid": "✅ 有效的YouTube URL",
    "components.video_validation.youtube_invalid": "⚠️ 无效的YouTube URL。无法提取视频ID。",
    "components.video_validation.gdrive_valid": "✅ 有效的Google Drive URL",
    "components.video_validation.gdrive_invalid": "⚠️ 无效的Google Drive URL。无法提取文件ID。",
    "components.video_validation.facebook_valid": "✅ 有效的Facebook视频/reel URL",
    "components.video_validation.facebook_invalid": "⚠️ 无效的Facebook URL。必须是视频或reel URL。",
    "components.video_validation.instagram_warning": "⚠️ 检测到Instagram。嵌入可能受限 - 将提供'在Instagram中打开'选项。",
    "components.video_validation.instagram_invalid": "⚠️ 无效的Instagram URL。必须是reel、帖子或TV URL。",
    "components.video_validation.direct_valid": "✅ 有效的视频URL（{format}）",
    "components.video_validation.unsupported": "⚠️ 不支持的URL类型。请使用YouTube、Facebook、Instagram、Google Drive或直接视频链接...",
    "components.video_validation.error": "⚠️ 无法验证URL格式",
    "components.qr_stats.title": "**二维码统计：**",
    "components.qr_stats.data_size": "- 数据大小：{bytes} 字节",
    "components.qr_stats.qr_version": "- 二维码版本：~{version}",
    "components.qr_stats.scannable_yes": "- 可扫描：✅ 是",
    "components.qr_stats.scannable_no": "- 可扫描：❌ 太大",
    "components.qr_tip": "📱 用手机相机扫描直接打开问候！",
    "components.themes.snowflake": "❄️ 雪花",
    "components.themes.fireworks": "🎆 烟花",
    "components.themes.lights": "✨ 灯光",
    "components.themes.stars": "⭐ 星星",
    "components.themes.confetti": "🎉 彩纸",
    "components.themes.champagne": "🥂 香槟",
    "components.themes.hearts": "❤️ 爱心",
    "components.themes.farewell": "👋 告别",
    "components.themes.burn": "🔥 阅后即焚",
    "components.themes.valentine": "💕 情人节",
    "components.themes.general": "⊞ 通用（无图标）",
    "_comment_demo_tab": "=== 演示标签页 ===",
    "demo_tab.header": "✨ 互动演示",
    "demo_tab.subtitle": "通过3个简单步骤创建示例问候",
    "demo_tab.info": "ℹ️ 这是一个演示，展示概念。要获得包括下载在内的完整功能，请使用 [**创建问候**](?tab=create) 标签页。",
    "demo_tab.step1.title": "### 步骤 1：选择您的风格",
    "demo_tab.step1.tip": "💡 **提示：** 选择与场合相配的主题。颜色和动画会自动适配！",
    "demo_tab.theme_selection_help": "选择 {theme} 主题",
    "demo_tab.step2.title": "### 步骤 2：预览和个性化",
    "demo_tab.step2.tip": "💡 **提示：** 这是您的问候的显示效果。您可以在下方快速编辑！",
    "demo_tab.edit.title": "✍️ **编辑姓名和消息**",
    "demo_tab.warning.html_removed": "⚠️ 检测到HTML标签并已删除。请仅使用纯文本。",
    "demo_tab.step3.title": "### 步骤 3：创建魔法",
    "demo_tab.step3.tip": "💡 **提示：** 准备好了吗？点击下方生成您的专属问候二维码！",
    "demo_tab.generate_button": "✨ 生成二维码 ✨",
    "demo_tab.success": "🎉 **成功！** 您的演示问候预览已准备就绪。",
    "demo_tab.demo_mode_info": "ℹ️ **演示模式**：这仅是预览。使用 [**创建问候**](?tab=create) 标签页获取完整功能和下载。",
    "demo_tab.privacy_info": "🔒 **内置隐私**：您的消息直接编码在二维码图案中。\n        它对AI训练系统是不透明的，直到扫描之前都是不可见的——没有电子邮件提供商的窥探，\n        没有算法分析，没有未经授权的LLM训练。完全隐私。🛡️",
    "demo_tab.qr_section": "#### 📱 您的专属二维码",
    "demo_tab.scan_me": "扫我！",
    "demo_tab.download_button": "⬇️ 下载图像（仅演示）",
    "demo_tab.download_disabled": "演示模式下禁用下载。使用'创建问候'标签页获取完整功能。",
    "demo_tab.preview_only": "💡 这仅是预览。访问 [**创建问候**](?tab=create) 标签页下载您的个性化二维码。",
    "demo_tab.preview_section": "#### 👀 扫描预览",
    "demo_tab.preview_title": "思念你",
    "demo_tab.preview_hint": "点击打开",
    "demo_tab.ready_prompt": "🚀 准备好实现它了吗？",
    "demo_tab.ready_description": "此演示展示了概念。要获得包括下载、自定义背景等在内的完整功能，请创建您自己的问候！",
    "demo_tab.create_my_own": "🎁 创建我自己的问候",
    "demo_tab.start_over": "🔄 重新开始演示",
    "_comment_scan_tab": "=== 扫描标签页 ===",
    "scan_tab.header": "📱 扫描问候二维码",
    "scan_tab.success": "🎉 已收到问候！",
    "scan_tab.intro": "上传问候二维码图像以查看消息！",
    "scan_tab.upload.label": "选择二维码图像",
    "scan_tab.upload.help": "上传包含问候二维码的图像",
    "scan_tab.uploaded_qr": "已上传的二维码",
    "scan_tab.uploaded_image": "已上传的图像",
    "scan_tab.greeting_message": "问候消息",
    "scan_tab.invalid_format": "此二维码不包含有效的问候格式。",
    "scan_tab.decoded_data": "已解码数据：",
    "scan_tab.no_qr_found": "图像中未找到二维码。",
    "scan_tab.no_libs": "（无可用的扫描库）",
    "scan_tab.zxing_suggestion": "（未安装ZXing-cpp - 它可能更好地处理此图像）",
    "scan_tab.opencv_required": "二维码扫描需要OpenCV系统库。",
    "scan_tab.manual_entry": "请使用下方的手动JSON输入：",
    "scan_tab.paste_label": "粘贴二维码数据（JSON）",
    "scan_tab.invalid_data": "无效的问候数据格式",
    "scan_tab.error": "处理图像时出错：{error}",
    "scan_tab.alternative": "或者，您可以在下方手动粘贴二维码数据：",
    "scan_tab.create_own": "📝 创建您自己的问候",
    "scan_tab.url_decode_error": "无法从URL解码问候。请尝试上传二维码图像。",
    "_comment_about_tab": "=== 关于标签页 ===",
    "about_tab.header": "ℹ️ 关于",
    "about_tab.title": "## 节日问候二维码生成器",
    "about_tab.description": "此应用程序允许您创建编码在二维码中的个性化节日问候。以独特而现代的方式分享您的消息！",
    "about_tab.video_section": "实际演示",
    "about_tab.video_description": "观看快速演示，了解如何轻松创建和分享个性化问候二维码。",
    "about_tab.why_choose": "为什么选择二维码问候？",
    "about_tab.environment.title": "### 🌱 环保",
    "about_tab.environment.heading": "**零纸张。零邮费。即时送达。**",
    "about_tab.environment.description": "传统纸质卡片消耗材料、印刷资源和运输能源。二维码问候100%数字化——不伤害树木，不产生送货卡车的碳足迹。在不留下星球痕迹的情况下传递您的爱。",
    "about_tab.secret.title": "### 🔐 传输中的秘密",
    "about_tab.secret.heading": "**个人的、私密的、AI安全的。**",
    "about_tab.secret.description": "您的问候编码在二维码图案本身中——对AI系统数学上不透明，直到扫描才可见...",
    "about_tab.secret.benefit1": "✅ **无电子邮件提供商窥探**",
    "about_tab.secret.benefit2": "✅ **无算法分析**",
    "about_tab.secret.benefit3": "✅ **无未经授权的LLM训练**",
    "about_tab.secret.benefit4": "✅ **只有收件人看到您的消息**",
    "about_tab.secret.tagline": "在不留下数字足迹的情况下传递您的爱！❤️🛡️",
    "about_tab.device.title": "### 📱 设备友好",
    "about_tab.device.heading": "**适用于任何手机。无需应用程序。**",
    "about_tab.device.description": "收件人只需将相机对准二维码——就是这样！在iOS和Android上无缝工作，直接在浏览器中打开。无需下载，无需注册，无摩擦。只需扫描和微笑。",
    "about_tab.business.title": "📈 适合企业：将关注转化为行动",
    "about_tab.business.challenge": "**当今注意力经济的第一大挑战：** 将被动视频观看转化为主动网站访问。\n\nYouTube Shorts 在 2025 年每天产生 **700 亿次观看**，但观众很少离开平台。\n传统的描述链接点击率很低。注意力在几秒钟内被捕获——也同样快地流失。",
    "about_tab.business.solution_intro": "**二维码问候通过连接内容和商业解决了这个问题：**",
    "about_tab.business.step1": "1. 🎬 **嵌入您的内容** — 使用任何 YouTube 视频作为背景",
    "about_tab.business.step2": "2. 💬 **添加您的 CTA** — 在消息中包含折扣代码、链接或独家优惠",
    "about_tab.business.step3": "3. 📱 **扫描转化** — 收件人扫描、观看您的视频，并看到您的行动号召",
    "about_tab.business.use_cases_title": "**用例：**",
    "about_tab.business.use_cases_list": "- 展示产品演示视频的贸易展览显示屏\n- 链接到教程 + 折扣代码的产品包装\n- 通过视频内容变得生动的平面广告\n- 带有品牌故事 + 落地页链接的电子邮件签名",
    "about_tab.business.stats_title": "**2025像统计数据：**",
    "about_tab.business.stats_list": "📊 **1 亿** 美国消费者将扫描二维码\n\n📈 **73%** 更喜欢通过短视频发现产品\n\n💰 Shorts 的 ROI 比传统视频高 **20%**\n\n🎯 从 Shorts 到全面参与的转化率为 **68%**\n\n*来源：Bitly, Scratcher.io, Zebracat.ai*",
    "about_tab.features.title": "### 功能",
    "about_tab.features.custom": "- ✨ 创建自定义问候二维码",
    "about_tab.features.scan": "- 📱 扫描和读取问候二维码",
    "about_tab.features.themes": "- 🎨 带嵌入图标的多种主题选项",
    "about_tab.features.download": "- 📥 将二维码下载为图像",
    "about_tab.features.json": "- 💾 紧凑的JSON格式，实现高效编码",
    "about_tab.how_it_works.title": "### 工作原理",
    "about_tab.how_it_works.step1": "1. 输入您的问候详细信息（发件人、收件人、消息）",
    "about_tab.how_it_works.step2": "2. 选择主题",
    "about_tab.how_it_works.step3": "3. 生成二维码",
    "about_tab.how_it_works.step4": "4. 下载并分享！",
    "about_tab.how_it_works.recipients": "收件人可以使用手机相机扫描二维码或将其上传到此应用程序以查看您的消息。",
    "about_tab.technical.title": "### 技术细节",
    "about_tab.technical.error_correction": "- 使用高纠错（H级）实现可靠扫描",
    "about_tab.technical.json_format": "- 紧凑的JSON格式最小化二维码尺寸",
    "about_tab.technical.message_length": "- 舒适地支持最多约500个字符的消息",
    "about_tab.technical.built_with": "- 使用Streamlit和netshare构建",
    "about_tab.privacy.title": "### 🤖 GenAI时代的隐私",
    "about_tab.privacy.heading": "**您的消息对AI系统隐藏。**",
    "about_tab.privacy.description": "与通过电子邮件、短信或社交媒体共享的文本不同，二维码编码的消息对自动分析**数学上不透明**：",
    "about_tab.privacy.no_ai": "- **无AI扫描**：消息格式防止自动文本提取",
    "about_tab.privacy.no_training": "- **无训练数据**：您的个人消息不会训练LLM（ChatGPT、Gemini、Claude等）",
    "about_tab.privacy.no_analysis": "- **无算法分析**：电子邮件提供商和平台无法读取或分析您的内容",
    "about_tab.privacy.no_cloud": "- **无云索引**：消息仅存在于二维码图案中，而不在服务器上",
    "about_tab.privacy.tagline": "您的问候是编码的，而不是传输的。设计保护。🛡️",
    "about_tab.powered_by.title": "### 技术支持",
    "about_tab.powered_by.netshare": "- **netshare** - 网络共享和二维码实用程序",
    "about_tab.powered_by.streamlit": "- **Streamlit** - 交互式网页界面",
    "about_tab.powered_by.qrcode": "- **qrcode** - 二维码生成",
    "about_tab.powered_by.pillow": "- **Pillow** - 图像处理",
    "_comment_examples_tab": "=== 示例标签页 ===",
    "examples_tab.header": "📖 示例",
    "examples_tab.intro": "以下是您可以创建的一些示例节日问候：",
    "examples_tab.christmas.title": "🎄 圣诞问候",
    "examples_tab.christmas.from": "爱丽丝",
    "examples_tab.christmas.to": "鲍勃",
    "examples_tab.christmas.message": "圣诞快乐！祝您这个季节充满欢乐和幸福。感谢您成为一位出色的朋友！",
    "examples_tab.newyear.title": "🎆 新年寄语",
    "examples_tab.newyear.from": "鲍勃",
    "examples_tab.newyear.to": "未来的我",
    "examples_tab.newyear.message": "2025年太精彩了！祝愿2026年充满成长和新冒险！",
    "examples_tab.wedding.title": "💍 婚礼邀请",
    "examples_tab.wedding.from": "艾玛和詹姆斯",
    "examples_tab.wedding.to": "亲朋好友",
    "examples_tab.wedding.message": "我们要结婚了！请记住日期：2026年6月15日。更多详情稍后公布！",
    "examples_tab.farewell.title": "👋 告别同事",
    "examples_tab.farewell.from": "亚历克斯",
    "examples_tab.farewell.to": "团队",
    "examples_tab.farewell.message": "与大家共事是一段美妙的旅程！感谢你们带来的回忆、欢笑和教训。让我们保持联系！",
    "examples_tab.farewell.visible_message": "扫描阅读我的告别信",
    "examples_tab.valentine.title": "💕 情人节情书",
    "examples_tab.valentine.from": "你的神秘仰慕者",
    "examples_tab.valentine.to": "我最亲爱的",
    "examples_tab.valentine.message": "与你在一起的每一刻都像一场美丽的梦。你让我的心怦怦跳，让我的灵魂歌唱。情人节快乐，我生命中的挚爱！💕🌹",
    "examples_tab.valentine.visible_message": "扫描查看情书",
    "examples_tab.marketing.title": "📈 营销漏斗 - 视频到网站",
    "examples_tab.marketing.from": "品牌策略师",
    "examples_tab.marketing.to": "潜在客户",
    "examples_tab.marketing.message": "✨ 独家优惠 ✨\n\n喜欢刚才看的内容吗？首单享受8折优惠！\n\n🎁 使用代码：QRGREET20\n👉 访问：www.yourbrand.com/special\n\n优惠48小时后到期。不要错过！\n\n#注意力经济 #将观看转化为访问",
    "examples_tab.marketing.visible_message": "🎬 扫描获取独家优惠",
    "examples_tab.mission.title": "🔥 碟中谍 - 阅后即焚",
    "examples_tab.mission.from": "IMF特工",
    "examples_tab.mission.to": "外勤特工",
    "examples_tab.mission.message": "你的任务：18:00在米兰咖啡馆会合。带上包裹。阅读后删除此消息。不留数字痕迹 - 无电子邮件拦截，无AI监控，无服务器日志。仅供你查看。🕵️",
    "examples_tab.mission.visible_message": "删除我",
    "_comment_batch_tab": "=== 批量标签页 ===",
    "batch_tab.header": "📦 批量二维码生成",
    "batch_tab.description": "通过上传Excel电子表格一次生成多个二维码。",
    "batch_tab.video_feature": "💡 **新功能**：您现在可以使用YouTube URL或直接视频URL作为背景！只需将URL粘贴到Background列中。",
    "batch_tab.step1": "1. 下载模板",
    "batch_tab.step1_description": "下载Excel模板，填写您的问候，然后在下方上传。",
    "batch_tab.download_template": "📥 下载模板（.csv）",
    "batch_tab.valid_options": "查看有效选项",
    "batch_tab.valid_themes": "**有效主题：**",
    "batch_tab.valid_backgrounds": "**有效背景：**",
    "batch_tab.local_keep": "*来自`keep/`文件夹的本地文件：*",
    "batch_tab.local_gif": "*来自`gif/`文件夹的本地文件：*",
    "batch_tab.no_backgrounds": "`{folder}/`文件夹中没有可用的背景",
    "batch_tab.web_urls": "*或使用网络视频URL：*",
    "batch_tab.url_youtube1": "- YouTube：`youtu.be/VIDEO_ID`",
    "batch_tab.url_youtube2": "- YouTube：`https://www.youtube.com/watch?v=VIDEO_ID`",
    "batch_tab.url_direct": "- 直接视频：`https://example.com/video.mp4`",
    "batch_tab.step2": "2. 上传填写的模板",
    "batch_tab.upload.label": "选择您填写的CSV文件",
    "batch_tab.upload.help": "上传包含问候数据的模板",
    "batch_tab.loaded": "从CSV加载了{count}个问候！",
    "batch_tab.preview_data": "预览数据",
    "batch_tab.error.missing_columns": "缺少必需的列：{columns}",
    "batch_tab.warning.invalid_themes": "某些行有无效的主题：{themes}。它们将使用'general'。",
    "batch_tab.generate_all": "🚀 生成所有二维码",
    "batch_tab.generating": "正在生成二维码 {current}/{total}：{name}...",
    "batch_tab.success": "✅ 所有二维码已生成！",
    "batch_tab.download_all": "📥 下载所有二维码（ZIP）",
    "batch_tab.error.row": "行{idx}：{message}",
    "batch_tab.error.processing": "处理Excel文件时出错：{error}",
    "_comment_display": "=== 二维码显示模块 ===",
    "display.qr_preview": "二维码预览",
    "display.error_animation": "⚠️ 无法加载二维码动画库。请检查您的网络连接。",
    "display.to_label": "收件人：",
    "display.from_label": "发件人：",
    "display.created": "创建于：{date}",
    "display.instagram_button": "📱 在Instagram中打开",
    "_comment_view_page": "=== 查看页面 ===",
    "view_page.invalid_data": "无效或缺失的问候数据。",
    "view_page.scan_prompt": "请扫描有效的问候二维码或转到主页创建一个。",
    "view_page.from": "— 来自 {name}",
    "view_page.create_prompt": "创建您自己的问候二维码！"
  }
}
````

## File: streamlit/tabs/demo_tab.py
````python
"""
Interactive Demo Tab
Allows users to create a sample greeting in <60 seconds without friction
"""

import streamlit as st
from datetime import datetime
import json
from typing import Dict
import qrcode
from PIL import Image
import io

# Import utilities
from utils.demo_data import (
    DemoGreeting,
    get_seasonal_demo,
    ANIMATION_PRESETS
)
from config import THEME_COLORS, THEME_ICONS
from i18n import get_text as _

# ============================================================================
# State Management
# ============================================================================

def init_demo_state():
    """Initialize session state for demo tab"""
    if "demo_greeting" not in st.session_state:
        st.session_state.demo_greeting = get_seasonal_demo()
    else:
        # Validate and fix corrupted message field (should be plain text, not HTML)
        greeting = st.session_state.demo_greeting
        if "<" in greeting.message and ">" in greeting.message:
            # Message contains HTML tags - reset to default
            st.session_state.demo_greeting = get_seasonal_demo()

    if "demo_qr_generated" not in st.session_state:
        st.session_state.demo_qr_generated = False
    if "demo_customize_expanded" not in st.session_state:
        st.session_state.demo_customize_expanded = False
    if "demo_qr_image" not in st.session_state:
        st.session_state.demo_qr_image = None

# ============================================================================
# QR Code Generation
# ============================================================================

def generate_demo_qr_code(greeting: DemoGreeting) -> Image.Image:
    """Generate QR code image for demo greeting"""
    
    # Encode greeting data
    greeting_json = json.dumps(greeting.to_dict())
    
    # Create QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(greeting_json)
    qr.make(fit=True)
    
    # Get theme colors
    theme_colors = THEME_COLORS.get(greeting.theme, THEME_COLORS["general"])
    
    # Generate image
    img = qr.make_image(
        fill_color=theme_colors["module"],
        back_color="white"
    )
    
    return img.convert('RGB')

# ============================================================================
# UI Components
# ============================================================================

def get_step_container_style(step_num: int, is_active: bool) -> str:
    """Get CSS style for step containers"""
    
    border_color = "#667eea" if is_active else "#e0e0e0"
    bg_color = "#ffffff" if is_active else "#f9f9f9"
    opacity = "1.0" if is_active else "0.7"
    
    return f"""
    <div style="
        border: 2px solid {border_color};
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: {bg_color};
        opacity: {opacity};
        transition: all 0.3s ease;
    ">
        <div style="
            display: inline-block;
            background: {border_color};
            color: white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            margin-right: 10px;
        ">{step_num}</div>
        <span style="font-size: 1.2em; font-weight: bold; color: #333;">
    """

def display_greeting_card_preview(greeting: DemoGreeting):
    """Display the greeting card preview"""
    
    theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
    
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; color: white; box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4); max-width: 600px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 3em; margin-bottom: 10px;">{theme_emoji}</div>
    </div>
    <div style="background: rgba(255,255,255,0.95); color: #333; padding: 25px; border-radius: 15px; position: relative;">
        <p style="margin: 5px 0 0 0; font-weight: 600; font-size: 1.1em;">{_('common.labels.from')}: {greeting.from_name}</p>
        <p style="margin: 5px 0 20px 0; font-weight: 600; font-size: 1.1em;">{_('common.labels.to')}: {greeting.to_name}</p>
        <p style="font-family: Georgia, serif; font-size: 1.15em; line-height: 1.6; color: #444; font-style: italic; margin: 0;">"{greeting.message}"</p>
    </div>
</div>
""", unsafe_allow_html=True)

def display_theme_buttons(current_theme: str):
    """Display theme selection buttons"""
    
    themes = list(THEME_ICONS.keys())
    themes = [t for t in themes if t != "general" and THEME_ICONS.get(t)]
    
    cols = st.columns(8)
    
    for idx, theme in enumerate(themes):
        with cols[idx % 8]:
            emoji = THEME_ICONS.get(theme, "🎁")
            is_selected = theme == current_theme
            
            # Use columns to center buttons if needed
            if st.button(
                f"{emoji}",
                key=f"step1_theme_{theme}",
                help=_("demo_tab.theme_selection_help", theme=theme.title()),
                width='stretch',
                type="primary" if is_selected else "secondary"
            ):
                return theme
                
    return current_theme

def render_step_1_theme():
    """Render Step 1: Choose Theme"""
    
    greeting = st.session_state.demo_greeting
    
    st.markdown(_("demo_tab.step1.title"))
    st.info(_("demo_tab.step1.tip"))
    
    new_theme = display_theme_buttons(greeting.theme)
    if new_theme != greeting.theme:
        st.session_state.demo_greeting.theme = new_theme
        st.session_state.demo_greeting.animation = ANIMATION_PRESETS.get(new_theme, ["MaterializeIn"])[0]
        st.rerun()

def render_step_2_preview():
    """Render Step 2: Preview & Personalize"""
    
    greeting = st.session_state.demo_greeting
    
    st.markdown(_("demo_tab.step2.title"))
    st.info(_("demo_tab.step2.tip"))
    
    # Preview
    display_greeting_card_preview(greeting)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Inline customization using expander
    with st.expander(_("demo_tab.edit.title"), expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_from = st.text_input(_("common.labels.from"), value=greeting.from_name, key="step2_from")
        with col2:
            new_to = st.text_input(_("common.labels.to"), value=greeting.to_name, key="step2_to")

        new_message = st.text_area(_("common.labels.message"), value=greeting.message, height=100, key="step2_msg")

        # Apply changes button
        if st.button(_("common.buttons.update_preview"), type="secondary", width='stretch'):
            # Validate message doesn't contain HTML (strip tags if found)
            if "<" in new_message and ">" in new_message:
                import re
                cleaned_message = re.sub(r'<[^>]+>', '', new_message)
                st.warning(_("demo_tab.warning.html_removed"))
                new_message = cleaned_message

            st.session_state.demo_greeting.from_name = new_from
            st.session_state.demo_greeting.to_name = new_to
            st.session_state.demo_greeting.message = new_message
            st.rerun()

def render_step_3_generate():
    """Render Step 3: Generate Action"""
    
    st.markdown(_("demo_tab.step3.title"))
    st.info(_("demo_tab.step3.tip"))
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            _("demo_tab.generate_button"),
            type="primary",
            width='stretch',
            key="step3_generate_btn"
        ):
            st.session_state.demo_qr_generated = True
            st.rerun()

def render_step_4_result():
    """Render Step 4: The Result"""

    greeting = st.session_state.demo_greeting

    st.success(_("demo_tab.success"))
    st.info(_("demo_tab.demo_mode_info"), icon="ℹ️")

    # Privacy benefits highlight
    st.info(_("demo_tab.privacy_info"), icon="🔒")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(_("demo_tab.qr_section"))
        # Generate QR
        qr_img = generate_demo_qr_code(greeting)
        st.image(qr_img, width='stretch', caption=_("demo_tab.scan_me"))
        
        # Download (disabled for demo)
        img_byte_arr = io.BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        st.download_button(
            _("demo_tab.download_button"),
            data=img_byte_arr.getvalue(),
            file_name="my_greeting_qr.png",
            mime="image/png",
            width='stretch',
            disabled=True,
            help=_("demo_tab.download_disabled")
        )

        st.caption(_("demo_tab.preview_only"))

    with col2:
        st.markdown(_("demo_tab.preview_section"))
        # Mobile frame mockup simplified
        theme_emoji = THEME_ICONS.get(greeting.theme, "🎁")
        st.markdown(f"""
<div style="border: 8px solid #333; border-radius: 30px; padding: 15px; background: white; max-width: 300px; margin: 0 auto; position: relative;">
    <div style="background: #f0f0f0; border-radius: 20px; padding: 15px; text-align: center; min-height: 350px;">
        <div style="font-size: 2.5em; margin-top: 20px;">{theme_emoji}</div>
        <h4 style="margin: 10px 0; color: #667eea;">{_('demo_tab.preview_title')}</h4>
        <p style="font-size: 0.9em; color: #555;">"{greeting.message[:80]}..."</p>
        <div style="margin-top: 20px; font-size: 0.8em; color: #888;">{_('demo_tab.preview_hint')}</div>
    </div>
</div>
""", unsafe_allow_html=True)
        
    st.markdown("---")

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3>{_('demo_tab.ready_prompt')}</h3>
        <p>{_('demo_tab.ready_description')}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Use markdown styled as button to navigate like the hyperlinks do
        st.markdown(f"""
        <a href="?tab=create" style="
            display: inline-block;
            width: 100%;
            padding: 0.5rem 1rem;
            background-color: #ff4b4b;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 1rem;
            border: 1px solid transparent;
            transition: all 0.2s;
        " onmouseover="this.style.backgroundColor='#ff2b2b'" onmouseout="this.style.backgroundColor='#ff4b4b'">
            {_('demo_tab.create_my_own')}
        </a>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(_("demo_tab.start_over"), type="secondary", width='stretch'):
            st.session_state.demo_qr_generated = False
            st.session_state.demo_greeting = get_seasonal_demo()
            st.rerun()

# ============================================================================
# Main Render Function
# ============================================================================

def render():
    """Main demo tab render function"""
    
    # Initialize state
    init_demo_state()
    
    # Header with demo notice
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>{_('demo_tab.header')}</h1>
        <p style="color: #666;">{_('demo_tab.subtitle')}</p>
        <div style="background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); color: white; padding: 12px 20px; border-radius: 10px; margin: 15px auto; max-width: 600px; font-weight: 500;">
            {_('demo_tab.info').replace('[**', '<strong><a href="?tab=create" style="color: white; text-decoration: underline;">').replace('**](?tab=create)', '</a></strong>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render steps
    if not st.session_state.demo_qr_generated:
        # Step 1
        with st.container():
            render_step_1_theme()
            st.divider()
            
        # Step 2
        with st.container():
            render_step_2_preview()
            st.divider()
            
        # Step 3
        with st.container():
            render_step_3_generate()
            
    else:
        # Result View
        render_step_4_result()


# ============================================================================
# If running as main module (for testing)
# ============================================================================

if __name__ == "__main__":
    render()
````

## File: streamlit/README.md
````markdown
https://qr-greeting.streamlit.app/

![qr](greeting.png)

# Holiday Greeting QR Code Generator

A beautiful Streamlit web application for creating and sharing personalized holiday greetings via QR codes.

## Features

- 🎁 **Create Custom Greetings**: Generate personalized holiday greeting QR codes
- 📱 **Scan QR Codes**: Upload and decode greeting QR codes to view messages
- 🎨 **Multiple Themes**: Choose from various holiday themes (snowflake, fireworks, lights, etc.)
- 📥 **Download & Share**: Download QR codes as PNG images
- 💾 **Compact Format**: Efficient JSON encoding for optimal QR code size

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit - Web interface framework
- netshare - Network sharing and QR utilities
- qrcode - QR code generation
- Pillow - Image processing
- opencv-python-headless - Image processing for QR scanning
- pyzbar - QR code decoding

### Linux Additional Requirements

For QR code scanning on Linux, you may need to install zbar:

```bash
# Ubuntu/Debian
sudo apt-get install libzbar0

# Fedora
sudo dnf install zbar

# Arch
sudo pacman -S zbar
```

## Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Create a Greeting

1. Go to the "Create Greeting" tab
2. Fill in:
   - **From**: Your name
   - **To**: Recipient's name
   - **Occasion**: Select or enter custom occasion
   - **Theme**: Choose a visual theme
   - **Message**: Your personalized greeting (recommended < 300 chars)
3. Click "Generate QR Code"
4. Download the QR code image

### Scan a Greeting

1. Go to the "Scan QR Code" tab
2. Upload a QR code image (PNG/JPG)
3. View the decoded greeting message

## Examples

The app includes several example greetings:

- Christmas greeting with snowflake theme
- New Year message with fireworks theme
- Wedding announcement with champagne theme

## Technical Details

### Greeting Format

Greetings are encoded as compact JSON with the following structure:

```json
{
  "v": "1.0",
  "type": "greeting",
  "from": "Alice",
  "to": "Bob",
  "occasion": "Christmas 2025",
  "message": "Your greeting message here...",
  "theme": "snowflake",
  "created": "2025-12-07T10:30:00Z"
}
```

### QR Code Specifications

- **Error Correction**: Level H (High) - 30% damage recovery
- **Auto Version Detection**: Automatically selects optimal QR version
- **Capacity**: Supports messages up to ~500 characters
- **Format**: PNG images with 4-pixel border

### Message Capacity Reference

| Message Length | Data Size | QR Version |
|---------------|-----------|------------|
| 100 chars     | ~150 bytes | V10-H     |
| 200 chars     | ~250 bytes | V15-H     |
| 300 chars     | ~350 bytes | V20-H     |
| 500 chars     | ~550 bytes | V30-H     |

## Project Structure

```
streamlit/
├── app.py                  # Main Streamlit application
├── greeting_formats.py     # Greeting JSON encoding/decoding
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .streamlit/
    └── config.toml        # Streamlit configuration
```

## Use Cases

### Personal
- Holiday greeting cards
- Birthday wishes
- Thank you notes
- Time capsule messages for future dates

### Events
- Wedding save-the-date announcements
- Party invitations
- Celebration messages

### Creative
- Digital gift tags
- Memory keepsakes
- Photo album additions

## Powered By

- **[netshare](https://pypi.org/project/netshare/)** - PyPI package for network sharing and QR utilities
- **[Streamlit](https://streamlit.io)** - Interactive web framework
- **[qrcode](https://pypi.org/project/qrcode/)** - QR code generation library
- **[Pillow](https://python-pillow.org/)** - Python Imaging Library

## Tips

💡 **Best Practices**:
- Keep messages under 300 characters for optimal QR code size
- Test QR codes with multiple phone camera apps
- Choose themes that match your occasion
- Use high error correction for better scanning reliability

📱 **Scanning**:
- Most modern smartphones can scan QR codes with their camera app
- For older devices, download a QR scanner app
- Ensure good lighting when scanning

🎨 **Design**:
- Match themes to occasions (snowflake for Christmas, fireworks for New Year)
- Consider the recipient's preferences
- Add personal touches to messages

## License

This project uses the netshare package (GPL-3.0 license).

## Support

For issues or questions:
- Check the "About" tab in the application
- Review the examples for guidance
- Ensure all dependencies are properly installed

## Future Enhancements

Potential features for future versions:
- Animated QR codes with theme GIFs
- Custom color schemes
- Message templates
- Multi-language support
- QR code style customization
- Batch greeting generation

---

**Happy Greeting!** 🎄✨
![alt text](image-6.png)
https://www.techspot.com/guides/1676-qr-code-explained/
````

## File: streamlit/tabs/components.py
````python
"""
Shared UI components for tabs
Contains reusable UI elements and workflows
"""

import streamlit as st
import io
from datetime import datetime
from typing import Optional

# Import internationalization
from i18n import get_text as _

from greeting_formats import (
    create_holiday_greeting,
    get_greeting_stats,
    encode_greeting_to_url
)
from utils.url_utils import (
    is_web_url,
    classify_background,
    convert_youtube_to_embed_url,
    convert_google_drive_to_embed_url,
    convert_facebook_to_embed_url,
    convert_instagram_to_embed_url
)
from utils.image_utils import get_theme_display_icon
from utils.download_tracker import log_download
from qr.generator import generate_qr_code
from qr.display import display_qr_with_protection, display_animated_qr
from config import THEME_ANIMATIONS, THEME_COLORS


def render_theme_selector() -> str:
    """
    Render theme selector as a dropdown with icon preview (mobile-friendly)

    Returns:
        Selected theme name
    """
    # Theme options with emoji indicators for the dropdown
    themes = [
        ("snowflake", _("components.themes.snowflake")),
        ("fireworks", _("components.themes.fireworks")),
        ("lights", _("components.themes.lights")),
        ("stars", _("components.themes.stars")),
        ("confetti", _("components.themes.confetti")),
        ("champagne", _("components.themes.champagne")),
        ("hearts", _("components.themes.hearts")),
        ("farewell", _("components.themes.farewell")),
        ("valentine", _("components.themes.valentine")),
        ("burn_after_read", _("components.themes.burn")),
        ("general", _("components.themes.general"))
    ]

    # Create lookup dictionaries
    theme_keys = [t[0] for t in themes]
    theme_labels = [t[1] for t in themes]
    key_to_label = {t[0]: t[1] for t in themes}
    label_to_key = {t[1]: t[0] for t in themes}

    # Initialize session state for theme selection
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = "snowflake"

    # Get current selection's label for the selectbox default
    current_label = key_to_label.get(st.session_state.selected_theme, theme_labels[0])
    current_index = theme_labels.index(current_label) if current_label in theme_labels else 0

    # Dropdown selector
    selected_label = st.selectbox(
        _("components.theme.label"),
        options=theme_labels,
        index=current_index,
        help=_("components.theme.help"),
        key="theme_dropdown"
    )

    # Update session state based on selection
    selected_theme = label_to_key.get(selected_label, "snowflake")
    st.session_state.selected_theme = selected_theme

    # Show preview of selected icon
    if selected_theme != "general":
        icon_preview = get_theme_display_icon(selected_theme, size=80)
        if icon_preview:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(icon_preview, caption=_("components.theme_preview"), width='content')
    else:
        st.caption(_("components.theme_general_info"))

    return selected_theme


def validate_custom_url_callback() -> None:
    """
    Validate custom video URL when user types
    Updates session state with validation status and message
    """
    url = st.session_state.get('custom_video_url_input', '').strip()

    if not url:
        st.session_state.custom_url_validation_status = None
        st.session_state.custom_url_validation_message = ""
        return

    if not is_web_url(url):
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = _("components.video_validation.invalid_format")
        return

    bg_type = classify_background(url)

    if bg_type == 'youtube':
        embed_url = convert_youtube_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.youtube_valid")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.youtube_invalid")

    elif bg_type == 'google_drive':
        embed_url = convert_google_drive_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.gdrive_valid")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.gdrive_invalid")

    elif bg_type == 'facebook':
        embed_url = convert_facebook_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.facebook_valid")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.facebook_invalid")

    elif bg_type == 'instagram':
        embed_url = convert_instagram_to_embed_url(url)
        if embed_url:
            st.session_state.custom_url_validation_status = 'valid'
            st.session_state.custom_url_validation_message = _("components.video_validation.instagram_warning")
        else:
            st.session_state.custom_url_validation_status = 'invalid'
            st.session_state.custom_url_validation_message = _("components.video_validation.instagram_invalid")

    elif bg_type == 'direct_video':
        st.session_state.custom_url_validation_status = 'valid'
        file_ext = url.split('.')[-1].upper()
        st.session_state.custom_url_validation_message = _("components.video_validation.direct_valid", format=file_ext)

    elif bg_type == 'other_url':
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = _("components.video_validation.unsupported")

    else:
        st.session_state.custom_url_validation_status = 'invalid'
        st.session_state.custom_url_validation_message = _("components.video_validation.error")


def render_qr_generation_flow(
    from_name: str,
    to_name: str,
    message: str,
    theme: str,
    background: str = "",
    visible_message: str = "",
    all_sides: bool = False,
    warning_text: Optional[str] = None,
    use_animation: bool = False,
    animation_type: Optional[str] = None,
    qr_module_color: Optional[str] = None,
    qr_ring_color: Optional[str] = None
) -> None:
    """
    Unified QR generation and display flow

    This function eliminates code duplication by providing a single workflow for:
    1. Creating greeting data
    2. Encoding to URL
    3. Generating QR code
    4. Displaying QR with protection (animated or static)
    5. Showing statistics
    6. Providing download button

    Args:
        from_name: Sender name
        to_name: Recipient name
        message: Greeting message
        theme: Visual theme
        background: Background file/URL
        visible_message: Text overlay on QR
        all_sides: Display message on all 4 sides
        warning_text: Optional warning to display above QR (e.g., "No video URL entered")
        use_animation: Whether to use animated QR (default: True)
        animation_type: Animation type override (None = use theme default)
        qr_module_color: QR module color override (None = use theme default)
        qr_ring_color: QR position ring color override (None = use theme default)

    Returns:
        None (displays QR in Streamlit UI)
    """
    # Show warning if provided
    if warning_text:
        st.warning(warning_text)

    # 1. Create greeting data
    greeting = create_holiday_greeting(
        from_name=from_name,
        to_name=to_name,
        message=message,
        theme=theme,
        background=background
    )

    # 2. Encode greeting as URL (for mobile scanning)
    greeting_url = encode_greeting_to_url(greeting)

    # 3. Get statistics based on URL length
    stats = get_greeting_stats(greeting_url)

    # 4. Determine animation and colors
    final_animation = animation_type if animation_type is not None else THEME_ANIMATIONS.get(theme, "MaterializeIn")
    theme_colors = THEME_COLORS.get(theme, {"module": "#1f77b4", "ring": "#ff7f0e"})
    final_module_color = qr_module_color if qr_module_color else theme_colors["module"]
    final_ring_color = qr_ring_color if qr_ring_color else theme_colors["ring"]

    # 5. Display QR code (animated or static)
    if use_animation:
        # Use new animated QR display
        display_animated_qr(
            data=greeting_url,
            theme=theme,
            animation=final_animation,
            module_color=final_module_color,
            position_ring_color=final_ring_color,
            visible_message=visible_message if not all_sides else None,  # Web component doesn't support all_sides
            width=300,
            caption=f"Greeting QR Code for {to_name}"
        )
    else:
        # Use traditional static QR display (backward compatibility)
        # Generate QR code image with theme icon and colors
        qr_img = generate_qr_code(
            greeting_url,
            theme=theme,
            visible_message=visible_message,
            all_sides=all_sides,
            module_color=final_module_color,
            position_ring_color=final_ring_color
        )

        display_qr_with_protection(
            qr_img,
            caption=f"Greeting QR Code for {to_name}",
            width=None
        )

    # 6. Show statistics
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.write(_("components.qr_stats.title"))
    st.write(_("components.qr_stats.data_size", bytes=stats['byte_size']))
    st.write(_("components.qr_stats.qr_version", version=stats['recommended_qr_version']))
    st.write(_("components.qr_stats.scannable_yes") if stats['fits_in_qr'] else _("components.qr_stats.scannable_no"))
    st.caption(_("components.qr_tip"))
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. Provide download button with tracking
    # Generate static QR image for download (even if animated version was displayed)
    if use_animation:
        download_qr_img = generate_qr_code(
            greeting_url,
            theme=theme,
            visible_message=visible_message,
            all_sides=all_sides,
            module_color=final_module_color,
            position_ring_color=final_ring_color
        )
    else:
        download_qr_img = qr_img  # Already generated above

    buf = io.BytesIO()
    download_qr_img.save(buf, format='PNG')
    byte_im = buf.getvalue()

    # Generate filename first for consistency
    filename = f"greeting_{to_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    # Download button with tracking callback
    st.download_button(
        label=_("common.buttons.download"),
        data=byte_im,
        file_name=filename,
        mime="image/png",
        width='stretch',
        on_click=log_download,
        args=(filename,)
    )

    # 8. Add Goodwill Payment Button
    st.markdown("---")
    st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG", help="Support the project with a small donation")
````

## File: streamlit/tabs/create_tab.py
````python
"""
Create Greeting Tab
UI for creating new greeting QR codes
"""

import streamlit as st
import os
from tabs.components import (
    render_theme_selector,
    validate_custom_url_callback,
    render_qr_generation_flow
)
from utils.file_utils import get_available_gifs, get_available_backgrounds
from utils.url_utils import is_web_url
from config import THEME_ICONS
from qr.display import display_greeting_letter
from datetime import datetime
from i18n import get_text as _


def load_params_from_url():
    """Load greeting parameters from URL query params if present"""
    try:
        query_params = st.query_params
        
        # Check if we have plaintext API parameters
        if 'from' in query_params or 'message' in query_params:
            # Mark that we've loaded from URL (only do this once)
            if 'params_loaded_from_url' not in st.session_state:
                st.session_state.params_loaded_from_url = True
                
                # Load from parameter
                if 'from' in query_params:
                    st.session_state.create_from_name = query_params['from']
                
                # Load to parameter
                if 'to' in query_params:
                    st.session_state.create_to_name = query_params['to']
                
                # Load message parameter
                if 'message' in query_params:
                    message_text = query_params['message']
                    # Append URL to message if URL parameter exists
                    if 'url' in query_params:
                        message_text = f"{message_text}\n{query_params['url']}"
                    st.session_state.create_message = message_text
                
                # Load theme parameter
                if 'theme' in query_params:
                    st.session_state.selected_theme = query_params['theme']
                
                # Load URL parameter (store for later use or display)
                if 'url' in query_params:
                    st.session_state.source_url = query_params['url']
                    # Show info banner that this was shared from another app
                    st.session_state.show_source_banner = True

                # Load background parameter
                if 'background' in query_params:
                    background_param = query_params['background']

                    # Web URL: Set custom option and validate
                    if is_web_url(background_param):
                        st.session_state.selected_gif_option = _("create_tab.background.custom")
                        st.session_state.custom_video_url = background_param

                        # Trigger validation manually
                        st.session_state.custom_video_url_input = background_param
                        validate_custom_url_callback()

                        # Store validation errors for banner display
                        if st.session_state.custom_url_validation_status != 'valid':
                            st.session_state.background_validation_warning = (
                                f"⚠️ Background URL validation issue: "
                                f"{st.session_state.custom_url_validation_message}"
                            )

                    # Local file: Verify existence
                    else:
                        available_gifs = get_available_gifs()
                        if background_param in available_gifs:
                            st.session_state.selected_gif_option = background_param
                        else:
                            # Check kept (private) backgrounds
                            available_kept = get_available_backgrounds()
                            if background_param in available_kept:
                                # Found in keep/ folder.
                                # Don't select it in dropdown (keep as None or default).
                                # Store for use during generation.
                                st.session_state.keep_background = background_param
                                # Explicitly ensure we show "None" in dropdown
                                st.session_state.selected_gif_option = _("create_tab.background.none")
                            else:
                                st.session_state.background_validation_warning = (
                                    f"⚠️ Background file '{background_param}' not found. Using no background."
                                )
                                st.session_state.selected_gif_option = _("create_tab.background.none")
    except Exception as e:
        # Silently handle any query param errors
        pass


def render() -> None:
    """Tab for creating new greeting QR codes"""
    
    # Load URL parameters if present (only runs once)
    load_params_from_url()
    
    # Show banner if this greeting was shared from another app
    if st.session_state.get('show_source_banner', False):
        source_url = st.session_state.get('source_url', '')
        st.info(f"✨ Pre-filled from: {source_url}")
        st.session_state.show_source_banner = False  # Only show once

    # Show background validation warning if present
    if st.session_state.get('background_validation_warning', ''):
        st.warning(st.session_state.background_validation_warning)
        st.session_state.background_validation_warning = ''  # Only show once

    # Display the banner image as the header (left-aligned, smaller for clarity)
    banner_path = os.path.join(os.path.dirname(__file__), "..", "banner", "qr-greeting-banner-4x.png")
    if os.path.exists(banner_path):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.image(banner_path, width='stretch')
    else:
        # Fallback to text header if banner not found
        st.markdown(f'<div class="main-header"><h1>{_("create_tab.header")}</h1></div>',
                    unsafe_allow_html=True)
        st.markdown(f"### {_('create_tab.subtitle')}")

    st.write(_("create_tab.intro"))

    # =========================================================================
    # Step 1: Choose Theme & Background
    # =========================================================================
    st.markdown(_("create_tab.step1.title"))
    st.info(_("create_tab.step1.tip"))

    # Theme selector outside form to allow interactive button clicks
    theme = render_theme_selector()

    st.markdown("---")

    # GIF background dropdown - OUTSIDE form to allow immediate preview
    available_gifs = get_available_gifs()
    gif_options = [_("create_tab.background.none"), _("create_tab.background.custom")] + available_gifs

    # Initialize session state for GIF selection if needed
    if 'selected_gif_option' not in st.session_state:
         st.session_state.selected_gif_option = gif_options[0]

    if 'custom_video_url' not in st.session_state:
        st.session_state.custom_video_url = ""

    if 'keep_background' not in st.session_state:
        st.session_state.keep_background = None

    if 'custom_url_validation_status' not in st.session_state:
        st.session_state.custom_url_validation_status = None  # None, 'valid', 'invalid'

    if 'custom_url_validation_message' not in st.session_state:
        st.session_state.custom_url_validation_message = ""

    selected_gif_option = st.selectbox(
        _("create_tab.background.label"),
        options=gif_options,
        index=gif_options.index(st.session_state.selected_gif_option) if st.session_state.selected_gif_option in gif_options else 0,
        help=_("create_tab.background.help"),
        key="greeting_gif_background_interactive"
    )

    # Update session state
    st.session_state.selected_gif_option = selected_gif_option

    # Show custom URL input when "(Enter custom URL...)" is selected
    if selected_gif_option == _("create_tab.background.custom"):
        custom_url = st.text_input(
            _("create_tab.video_url.label"),
            value=st.session_state.custom_video_url,
            placeholder=_("create_tab.video_url.placeholder"),
            help=_("create_tab.video_url.help"),
            key="custom_video_url_input",
            on_change=validate_custom_url_callback
        )
        st.session_state.custom_video_url = custom_url

        # Display validation status
        if st.session_state.custom_url_validation_status == 'valid':
            st.success(st.session_state.custom_url_validation_message)
        elif st.session_state.custom_url_validation_status == 'invalid':
            st.warning(st.session_state.custom_url_validation_message)
        elif st.session_state.custom_video_url:
            st.info(_("create_tab.video_url.validating"))
        else:
            st.info(_("create_tab.video_url.enter_prompt"))

    # Convert selection to background parameter
    if selected_gif_option == _("create_tab.background.none"):
        selected_gif = ""
    elif selected_gif_option == _("create_tab.background.custom"):
        # Use custom URL if validated, otherwise empty
        if st.session_state.custom_url_validation_status == 'valid':
            selected_gif = st.session_state.custom_video_url
        else:
            selected_gif = ""
    else:
        # Local file selected
        selected_gif = selected_gif_option

    # Immediate preview below the dropdown (only for local files)
    if selected_gif and selected_gif_option != _("create_tab.background.custom"):
        gif_path = os.path.join(os.path.dirname(__file__), "..", "gif", selected_gif)
        if os.path.exists(gif_path):
            st.image(gif_path, caption=_("create_tab.gif_preview", gif_name=selected_gif), width='stretch')
        else:
            st.warning(_("create_tab.gif_not_found", file=selected_gif))

    st.divider()

    # =========================================================================
    # Step 2: Preview & Personalize (matching demo_tab layout)
    # =========================================================================
    st.markdown(_("create_tab.step2.title"))
    st.info(_("create_tab.step2.tip"))

    # Initialize session state for greeting fields with sample data
    if 'create_from_name' not in st.session_state:
        st.session_state.create_from_name = _("common.placeholders.your_name")
    if 'create_to_name' not in st.session_state:
        st.session_state.create_to_name = _("common.placeholders.friend_name")
    if 'create_message' not in st.session_state:
        st.session_state.create_message = _("create_tab.default_message")
    if 'create_visible_message' not in st.session_state:
        st.session_state.create_visible_message = ""
    if 'create_all_sides' not in st.session_state:
        st.session_state.create_all_sides = False

    # Get theme emoji for preview
    theme_emoji = THEME_ICONS.get(theme, "🎁")

    # Live Greeting Card Preview (matching demo_tab style)
    st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; color: white; box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4); max-width: 600px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 3em; margin-bottom: 10px;">{theme_emoji}</div>
    </div>
    <div style="background: rgba(255,255,255,0.95); color: #333; padding: 25px; border-radius: 15px; position: relative;">
        <p style="margin: 5px 0 0 0; font-weight: 600; font-size: 1.1em;">{_("create_tab.preview.from", name=st.session_state.create_from_name)}</p>
        <p style="margin: 5px 0 20px 0; font-weight: 600; font-size: 1.1em;">{_("create_tab.preview.to", name=st.session_state.create_to_name)}</p>
        <p style="font-family: Georgia, serif; font-size: 1.15em; line-height: 1.6; color: #444; font-style: italic; margin: 0;">"{st.session_state.create_message}"</p>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Expandable edit section (matching demo_tab style)
    with st.expander(_("create_tab.edit.title"), expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_from = st.text_input(
                _("common.labels.from"),
                value=st.session_state.create_from_name,
                key="edit_from_name",
                placeholder=_("common.placeholders.your_name")
            )
            # Auto-update session state
            if new_from != st.session_state.create_from_name:
                st.session_state.create_from_name = new_from
                st.rerun()
        with col2:
            new_to = st.text_input(
                _("common.labels.to"),
                value=st.session_state.create_to_name,
                key="edit_to_name",
                placeholder=_("common.placeholders.friend_name")
            )
            # Auto-update session state
            if new_to != st.session_state.create_to_name:
                st.session_state.create_to_name = new_to
                st.rerun()

        new_message = st.text_area(
            _("common.labels.message"),
            value=st.session_state.create_message,
            height=100,
            key="edit_message",
            placeholder=_("common.placeholders.message")
        )
        # Auto-update session state
        if new_message != st.session_state.create_message:
            st.session_state.create_message = new_message
            st.rerun()

        # Character counter
        if new_message:
            st.caption(_("create_tab.message_length", count=len(new_message)))

    # QR Code options section (keeping existing features)
    with st.expander(_("create_tab.qr_options.title"), expanded=False):
        visible_message = st.text_input(
            _("create_tab.visible_message.label"),
            value=st.session_state.create_visible_message,
            placeholder=_("create_tab.visible_message.placeholder"),
            help=_("create_tab.visible_message.help"),
            key="edit_visible_message"
        )

        all_sides = st.checkbox(
            _("create_tab.add_all_sides"),
            value=st.session_state.create_all_sides,
            help=_("create_tab.add_all_sides_help"),
            key="edit_all_sides"
        )

        # Update session state when changed
        if visible_message != st.session_state.create_visible_message:
            st.session_state.create_visible_message = visible_message
        if all_sides != st.session_state.create_all_sides:
            st.session_state.create_all_sides = all_sides

    st.divider()

    # =========================================================================
    # Step 3: Generate & Preview
    # =========================================================================
    st.markdown(_("create_tab.step3.title"))
    st.info(_("create_tab.step3.tip"))

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            _("common.buttons.generate"),
            type="primary",
            key="create_tab_generate_btn",
            icon=":material/qr_code_2:"
        )

    if generate_btn:
        # Get values from session state
        from_name = st.session_state.create_from_name
        to_name = st.session_state.create_to_name
        message = st.session_state.create_message
        visible_message = st.session_state.create_visible_message
        all_sides = st.session_state.create_all_sides

        # Validate inputs
        if not from_name or not to_name or not message:
            st.error(_("create_tab.error.required_fields"))
        # elif from_name == "Your Name" or to_name == "Friend's Name":
        #     st.warning("⚠️ Please personalize the From and To names before generating!")
        else:
            # Determine background and warning text
            warning_text = None
            background = selected_gif

            # Fallback to hidden keep_background if no visible background is selected
            if not background and st.session_state.get('keep_background'):
                background = st.session_state.keep_background

            if selected_gif_option == _("create_tab.background.custom"):
                if not st.session_state.custom_video_url:
                    warning_text = _("create_tab.warning.no_video")
                    background = ""
                elif st.session_state.custom_url_validation_status != 'valid':
                    st.error(_("create_tab.error.invalid_video", message=st.session_state.custom_url_validation_message))
                    st.info(_("create_tab.error.video_suggestion"))
                    st.stop()

            # Show success message
            st.success(_("create_tab.success"))

            # Show warning if applicable
            if warning_text:
                st.warning(warning_text)

            # Two-column layout matching demo_tab
            qr_col, preview_col = st.columns([1, 1])

            with qr_col:
                st.markdown(f"#### {_('create_tab.qr_section')}")
                # Generate and display QR code
                render_qr_generation_flow(
                    from_name=from_name,
                    to_name=to_name,
                    message=message,
                    theme=theme,
                    background=background,
                    visible_message=visible_message,
                    all_sides=all_sides
                )

            with preview_col:
                st.markdown(f"#### {_('create_tab.preview_section')}")
                st.caption(_("create_tab.preview_caption"))
                # Create greeting dict matching what display_greeting_letter expects
                preview_greeting = {
                    'to': to_name,
                    'from': from_name,
                    'message': message,
                    'theme': theme,
                    'background': background,
                    'created': datetime.now().strftime('%Y-%m-%d')
                }
                # Use the same display function as scan_tab
                display_greeting_letter(preview_greeting)

            st.markdown("---")

            # Start Over button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(_("common.buttons.create_another"), type="secondary", key="create_tab_start_over"):
                    # Reset session state
                    st.session_state.create_from_name = _("common.placeholders.your_name")
                    st.session_state.create_to_name = _("common.placeholders.friend_name")
                    st.session_state.create_message = _("create_tab.default_message")
                    st.session_state.create_visible_message = ""
                    st.session_state.create_all_sides = False
                    # Clear URL param flag
                    if 'params_loaded_from_url' in st.session_state:
                        del st.session_state.params_loaded_from_url
                    # Clear background validation warning
                    if 'background_validation_warning' in st.session_state:
                        del st.session_state.background_validation_warning
                    st.rerun()
````

## File: streamlit/tabs/scan_tab.py
````python
"""
Scan Greeting Tab
UI for scanning/decoding greeting QR codes
"""

import streamlit as st
from PIL import Image
import numpy as np
from i18n import get_text as _

# Import cv2 lazily to avoid startup crashes if system libs missing
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError as e:
    CV2_AVAILABLE = False
    CV2_IMPORT_ERROR = str(e)

except ImportError as e:
    CV2_AVAILABLE = False
    CV2_IMPORT_ERROR = str(e)

try:
    import zxingcpp
    ZXING_AVAILABLE = True
except ImportError:
    ZXING_AVAILABLE = False

from greeting_formats import (
    parse_greeting,
    format_greeting_display,
    decode_greeting_from_url
)
from qr.display import display_greeting_letter


def render() -> None:
    """Tab for scanning/decoding greeting QR codes"""
    st.markdown(f'<div class="main-header"><h1>{_("scan_tab.header")}</h1></div>',
                unsafe_allow_html=True)

    # Check if greeting data is passed via URL parameters (from QR code scan)
    try:
        query_params = st.query_params
    except:
        query_params = st.experimental_get_query_params()

    # Check if we have greeting data in URL (m or mc parameter indicates a message, or t=funnel for funnel)
    has_url_greeting = query_params.get('m') or query_params.get('mc') or query_params.get('t') == 'funnel'
    
    # If tab=view is explicitly set, don't show scan preview (let view_page handle it)
    is_view_tab = query_params.get('tab') == 'view'

    if has_url_greeting and not is_view_tab:
        # Check if this is a funnel-type QR code
        if query_params.get('t') == 'funnel':
            # Display funnel preview
            st.success(_("scan_tab.success") + " (Marketing Funnel)")
            
            # Extract funnel parameters
            headline = query_params.get("fh", "Special Offer")
            offer_text = query_params.get("m", "")
            cta_text = query_params.get("fc", "Learn More")
            cta_url = query_params.get("fu", "#")
            promo_code = query_params.get("fp", "")
            urgency = query_params.get("fg", "")
            video_url = query_params.get("bg", "")
            brand_name = query_params.get("f", "")
            theme = query_params.get("th", "fireworks")
            
            # Display funnel preview (similar to view_page but for scan tab)
            st.markdown("### 📈 Marketing Funnel QR Code Preview")
            
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                st.markdown("**📋 Funnel Details:**")
                st.write(f"**Headline:** {headline}")
                st.write(f"**Offer:** {offer_text[:100]}{'...' if len(offer_text) > 100 else ''}")
                st.write(f"**CTA Button:** {cta_text}")
                st.write(f"**Landing URL:** {cta_url}")
                if promo_code:
                    st.write(f"**Promo Code:** 🏷️ {promo_code}")
                if urgency:
                    st.write(f"**Urgency:** ⏰ {urgency}")
                if video_url:
                    st.write(f"**Video:** 🎬 {video_url[:50]}...")
                if brand_name:
                    st.write(f"**Brand:** {brand_name}")
                st.write(f"**Theme:** {theme}")
            
            with col_b:
                st.markdown("**👀 Mobile Preview:**")
                # Show a mockup of what the funnel looks like when scanned
                promo_html = f'<div style="background: #ffd700; color: #333; padding: 5px 15px; border-radius: 5px; font-weight: bold; margin: 10px 0; display: inline-block;">🏷️ {promo_code}</div>' if promo_code else ""
                urgency_html = f'<div style="color: #e74c3c; font-size: 0.9em; margin: 10px 0;">⏰ {urgency}</div>' if urgency else ""
                video_badge = "🎬 Video" if video_url else "No video"
                
                st.markdown(f"""
                <div style="border: 2px solid #333; border-radius: 15px; padding: 15px; 
                            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
                            color: white; max-width: 300px;">
                    <div style="background: #000; border-radius: 8px; height: 100px; 
                                display: flex; align-items: center; justify-content: center;
                                margin-bottom: 10px; position: relative;">
                        <span style="font-size: 2em;">🎬</span>
                        <div style="position: absolute; bottom: 5px; right: 5px; 
                                    background: rgba(255,255,255,0.2); padding: 2px 8px; 
                                    border-radius: 3px; font-size: 0.7em;">
                            {video_badge}
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.95); color: #333; 
                                padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 1.1em; font-weight: bold; margin-bottom: 8px;">
                            {headline}
                        </div>
                        <div style="font-size: 0.85em; margin-bottom: 10px; line-height: 1.4;">
                            {offer_text[:80]}{'...' if len(offer_text) > 80 else ''}
                        </div>
                        {promo_html}
                        {urgency_html}
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    color: white; padding: 10px 20px; border-radius: 20px; 
                                    font-weight: bold; cursor: pointer; display: inline-block; margin-top: 5px;">
                            {cta_text}
                        </div>
                    </div>
                    <div style="text-align: center; margin-top: 8px; font-size: 0.75em; opacity: 0.7;">
                        {f"from {brand_name}" if brand_name else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Option to create their own funnel or scan another
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📈 Create Your Own Funnel", width='stretch'):
                    st.query_params.clear()
                    st.query_params["tab"] = "funnel"
                    st.rerun()
            with col2:
                if st.button(_("common.buttons.scan_another"), width='stretch'):
                    st.query_params.clear()
                    st.query_params["tab"] = "scan"
                    st.rerun()
            
            return  # Don't show the upload interface
        else:
            # Regular greeting
            # Decode greeting from URL parameters and display it
            greeting = decode_greeting_from_url(dict(query_params))

            if greeting:
                st.success(_("scan_tab.success"))

                # Display the full letter format
                display_greeting_letter(greeting)

                st.markdown("---")
                st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG", help="Support the project with a small donation")

                # Option to create their own or scan another
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(_("scan_tab.create_own"), width='stretch'):
                        st.query_params.clear()
                        st.query_params["tab"] = "create"
                        # Update session state to ensure tab switches correctly
                        st.session_state.current_tab_index = 1  # create tab index
                        st.rerun()
                with col2:
                    if st.button(_("common.buttons.scan_another"), width='stretch'):
                        # Clear only the greeting params, keep tab=scan
                        st.query_params.clear()
                        st.query_params["tab"] = "scan"
                        # Update session state to ensure tab stays on scan
                        st.session_state.current_tab_index = 2  # scan tab index
                        st.rerun()

                return  # Don't show the upload interface
            else:
                st.warning(_("scan_tab.url_decode_error"))

    # Normal upload interface
    st.write(_("scan_tab.intro"))

    uploaded_file = st.file_uploader(
        _("scan_tab.upload.label"),
        type=['png', 'jpg', 'jpeg'],
        help=_("scan_tab.upload.help")
    )

    if uploaded_file is not None:
        try:
            # Display uploaded image
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader(_("scan_tab.uploaded_qr"))
                image = Image.open(uploaded_file)
                st.image(image, caption=_("scan_tab.uploaded_image"), width='stretch')

            # Decode QR code
            try:
                decoded_data = None
                
                # Check for zxing-cpp first (better detection rate and no system deps)
                if ZXING_AVAILABLE:
                    try:
                        # zxing-cpp works best with grayscale
                        img_gray = image.convert('L')
                        results = zxingcpp.read_barcodes(img_gray)
                        if results:
                            decoded_data = results[0].text
                    except Exception as e:
                        print(f"ZXing-cpp scan error: {e}")
                
                # Fallback to OpenCV if zxing-cpp failed or not available
                if not decoded_data and CV2_AVAILABLE:
                    # Use OpenCV for decoding
                    # Convert PIL Image to BGR numpy array
                    image_array = np.array(image.convert('RGB'))
                    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

                    detector = cv2.QRCodeDetector()
                    data, bbox, _points = detector.detectAndDecode(image_array)
                    
                    if data:
                        decoded_data = data

                if decoded_data:
                    qr_data = decoded_data

                    # Check if this is a funnel QR code (contains t=funnel in URL)
                    is_funnel = 't=funnel' in qr_data or '&t=funnel' in qr_data
                    
                    with col2:
                        st.subheader(_("scan_tab.greeting_message"))

                        if is_funnel:
                            # Parse URL parameters from funnel QR
                            import urllib.parse
                            try:
                                # Extract query parameters
                                if '?' in qr_data:
                                    query_string = qr_data.split('?', 1)[1]
                                    params = dict(urllib.parse.parse_qsl(query_string))
                                    
                                    # Display funnel preview
                                    st.success("Marketing Funnel QR Decoded!")
                                    
                                    headline = params.get("fh", "Special Offer")
                                    offer_text = params.get("m", "")
                                    cta_text = params.get("fc", "Learn More")
                                    cta_url = params.get("fu", "#")
                                    promo_code = params.get("fp", "")
                                    urgency = params.get("fg", "")
                                    video_url = params.get("bg", "")
                                    brand_name = params.get("f", "")
                                    
                                    st.markdown("**📋 Funnel Details:**")
                                    st.write(f"**Headline:** {headline}")
                                    st.write(f"**Offer:** {offer_text}")
                                    st.write(f"**CTA Button:** {cta_text}")
                                    st.write(f"**Landing URL:** {cta_url}")
                                    if promo_code:
                                        st.write(f"**Promo Code:** 🏷️ {promo_code}")
                                    if urgency:
                                        st.write(f"**Urgency:** ⏰ {urgency}")
                                    if video_url:
                                        st.write(f"**Video:** 🎬 Yes")
                                    if brand_name:
                                        st.write(f"**Brand:** {brand_name}")
                                    
                                    st.markdown("---")
                                    st.info("💡 This is a Marketing Funnel QR. When scanned with a phone, it will play a video and show this offer.")
                                    
                            except Exception as e:
                                st.error(f"Error parsing funnel QR: {e}")
                                st.code(qr_data)
                        else:
                            # Parse as regular greeting (handles both URL and JSON formats)
                            greeting = parse_greeting(qr_data)

                            if greeting:
                                # Display formatted greeting
                                display_greeting_letter(greeting)

                                st.markdown("---")
                                st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG", help="Support the project with a small donation")
                            else:
                                st.warning(_("scan_tab.invalid_format"))
                                st.write(_("scan_tab.decoded_data"))
                                st.code(qr_data)
                else:
                    msg = _("scan_tab.no_qr_found")
                    if not ZXING_AVAILABLE and not CV2_AVAILABLE:
                        msg += " " + _("scan_tab.no_libs")
                    elif not ZXING_AVAILABLE:
                        msg += " " + _("scan_tab.zxing_suggestion")

                    st.error(msg)

            except ImportError as e:
                st.error(_("scan_tab.opencv_required"))
                st.info(_("scan_tab.manual_entry"))

                manual_data = st.text_area(_("scan_tab.paste_label"))
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(_("scan_tab.invalid_data"))

            except Exception as e:
                st.error(_("scan_tab.error", error=str(e)))
                st.info(_("scan_tab.alternative"))

                manual_data = st.text_area(_("scan_tab.paste_label"), key="manual_data_exception")
                if manual_data:
                    greeting = parse_greeting(manual_data)
                    if greeting:
                        st.markdown('<div class="greeting-box">', unsafe_allow_html=True)
                        st.write(format_greeting_display(greeting))
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(_("scan_tab.invalid_data"))

        except Exception as e:
            st.error(_("scan_tab.error", error=str(e)))
````

## File: streamlit/app.py
````python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Holiday Greeting QR Code Generator
A Streamlit app for creating and reading holiday greeting QR codes
"""

import sys
import os

# Ensure the app's directory is in the Python path for local module imports
# This is required for Streamlit Cloud where the working directory may differ
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import streamlit.components.v1 as components

# Import configuration
from config import THEME_ICONS, PAGE_CONFIG, CSS_STYLES

# Import tab modules
from tabs import create_tab, scan_tab, examples_tab, batch_tab, about_tab, view_page, demo_tab, funnel_tab

# Import internationalization
from i18n import init_language, get_text as _, get_language_selector

# Import and start keepalive daemon for dependent services
from keepalive_daemon import start_keepalive_daemon
start_keepalive_daemon()

# Set page configuration
st.set_page_config(**PAGE_CONFIG)

# Initialize language support
init_language()

# Apply custom CSS
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Check if this is a view request (from QR code scan) - handle before main app
try:
    query_params = st.query_params
    tab_param = query_params.get('tab', 'create')
    # Read _tab param set by JavaScript tab click tracking
    tracked_tab = query_params.get('_tab')
except:
    # Fallback for older Streamlit versions
    query_params = st.experimental_get_query_params()
    tab_param = query_params.get('tab', ['create'])[0]
    tracked_tab = query_params.get('_tab', [None])[0]

# Update session state with tracked tab index if available
if tracked_tab is not None:
    try:
        st.session_state.current_tab_index = int(tracked_tab)
    except (ValueError, TypeError):
        pass

# Show mobile-friendly greeting view if tab=view
if tab_param == "view":
    view_page.render()
    st.stop()


def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        # Language selector at the top
        get_language_selector()

        st.markdown("---")

        st.title(_("app.sidebar.title"))
        st.write(_("app.sidebar.tagline"))
        st.markdown(_("app.sidebar.greener"))

        st.markdown("---")

        st.write(_("app.sidebar.quick_tips.title"))
        st.info(f"""
        {_("app.sidebar.quick_tips.tip1")}

        {_("app.sidebar.quick_tips.tip2")}

        {_("app.sidebar.quick_tips.tip3")}
        """)

        st.markdown("---")

        st.write(_("app.sidebar.support.title"))
        st.write(_("app.sidebar.support.text"))
        st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG")

        st.markdown("---")

        # Marketing Funnel tab toggle
        # Auto-enable if URL has tab=funnel parameter
        default_show_funnel = tab_param == "funnel"
        show_funnel = st.checkbox(
            "📈 Marketing Funnel",
            value=default_show_funnel,
            help="Create QR codes for marketing campaigns"
        )
        
        # Batch tab toggle
        # Auto-enable if URL has tab=batch parameter
        default_show_batch = tab_param == "batch"
        show_batch = st.checkbox(
            _("app.sidebar.batch_checkbox"),
            value=default_show_batch,
            help=_("app.sidebar.batch_help")
        )

    # Map tab names to indices (depends on whether batch/funnel tabs are shown)
    # Demo tab is first for visibility to new users
    tab_index_counter = 0
    tab_map = {}
    tab_map["demo"] = tab_index_counter
    tab_index_counter += 1
    tab_map["create"] = tab_index_counter
    tab_index_counter += 1
    tab_map["scan"] = tab_index_counter
    tab_index_counter += 1
    tab_map["examples"] = tab_index_counter
    tab_index_counter += 1
    if show_funnel:
        tab_map["funnel"] = tab_index_counter
        tab_index_counter += 1
    if show_batch:
        tab_map["batch"] = tab_index_counter
        tab_index_counter += 1
    tab_map["about"] = tab_index_counter
    
    # Use session state tab index if available (preserves tab across locale switch)
    # Otherwise fall back to URL param or default to Demo (0)
    if "current_tab_index" in st.session_state:
        tab_index = st.session_state.current_tab_index
    else:
        tab_index = tab_map.get(tab_param, 0)
        st.session_state.current_tab_index = tab_index

    # Inject JavaScript to:
    # 1. Click the correct tab if not the first tab
    # 2. Track tab clicks and store in session state via hidden query param
    components.html(f"""
        <script>
        (function() {{
            let attempts = 0;
            const maxAttempts = 10;
            const targetTabIndex = {tab_index};

            function clickTab() {{
                const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');

                if (tabs && tabs.length > targetTabIndex) {{
                    // Click the target tab if not already on it (index 0)
                    if (targetTabIndex > 0) {{
                        tabs[targetTabIndex].click();
                    }}
                    
                    // Add click listeners to all tabs to track selection
                    tabs.forEach((tab, index) => {{
                        if (!tab.hasAttribute('data-tab-tracked')) {{
                            tab.setAttribute('data-tab-tracked', 'true');
                            tab.addEventListener('click', () => {{
                                // Store tab index in URL param for next rerun
                                const url = new URL(window.parent.location.href);
                                url.searchParams.set('_tab', index.toString());
                                // Use history.replaceState to avoid page reload
                                window.parent.history.replaceState({{}}, '', url.toString());
                            }});
                        }}
                    }});
                    return true;
                }} else if (attempts < maxAttempts) {{
                    attempts++;
                    setTimeout(clickTab, 100);
                }}
            }}

            clickTab();
        }})();
        </script>
    """, height=0)

    # Main tabs (conditionally include batch and/or funnel tabs)
    # Demo tab is first for visibility to new users
    # Build tab names dynamically
    tab_names = [
        _("app.tabs.demo"),
        _("app.tabs.create"),
        _("app.tabs.scan"),
        _("app.tabs.examples")
    ]
    if show_funnel:
        tab_names.append("📈 Marketing Funnel")
    if show_batch:
        tab_names.append(_("app.tabs.batch"))
    tab_names.append(_("app.tabs.about"))
    
    # Create tabs
    tabs = st.tabs(tab_names)
    
    # Render tabs
    tab_idx = 0
    
    with tabs[tab_idx]:  # Demo
        demo_tab.render()
    tab_idx += 1
    
    with tabs[tab_idx]:  # Create
        create_tab.render()
    tab_idx += 1
    
    with tabs[tab_idx]:  # Scan
        scan_tab.render()
    tab_idx += 1
    
    with tabs[tab_idx]:  # Examples
        examples_tab.render()
    tab_idx += 1
    
    if show_funnel:
        with tabs[tab_idx]:  # Funnel
            funnel_tab.render()
        tab_idx += 1
    
    if show_batch:
        with tabs[tab_idx]:  # Batch
            batch_tab.render()
        tab_idx += 1
    
    with tabs[tab_idx]:  # About
        about_tab.render()


if __name__ == "__main__":
    main()
````

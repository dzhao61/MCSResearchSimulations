# Successful main-thesis builds always refresh the named delivery set.
# Historical drafts and explicitly different TeX targets are left alone.
use Cwd qw(abs_path);
use File::Basename qw(dirname);
use File::Spec;

my $welch_thesis_root = abs_path(dirname(__FILE__));
$pdf_mode = 1;
$out_dir = 'build';
@default_files = ('main.tex');

foreach my $directory ('build', 'build/chapters_rewrite', 'build/appendices_rewrite') {
    my $path = File::Spec->catdir($welch_thesis_root, $directory);
    mkdir $path unless -d $path;
}

sub welch_publish_delivery {
    my ($source, $pdf) = @_;
    my $main = File::Spec->catfile($welch_thesis_root, 'main.tex');
    return 0 unless defined(abs_path($source)) && abs_path($source) eq $main;
    my $python = File::Spec->catfile($welch_thesis_root, '..', '..', '.venv', 'bin', 'python');
    $python = 'python3' unless -x $python;
    my $script = File::Spec->catfile($welch_thesis_root, 'package_deliverables.py');
    my $status = system($python, $script, '--publish-built', $pdf);
    die "Delivery refresh failed; previous delivery files were preserved.\n" if $status != 0;
    return 0;
}

$success_cmd = 'internal welch_publish_delivery %T %D';
